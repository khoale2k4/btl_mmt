import { GroupedData } from '../interfaces/grouped_data.interface';
import { SearchAddition } from '../interfaces/search_addition.interface';
import { SearchCriteria } from '../interfaces/search_criteria.interface';
import {
  Op,
  FindOptions,
  ModelStatic,
  Model,
  Sequelize,
  IncludeOptions,
  Transaction,
  fn,
  col,
} from 'sequelize';

type AutoInclude = {
  option: 'auto';
  dbSource: Sequelize;
};

type ManualInClude = {
  option: 'manual';
  includeOption: IncludeOptions[];
};

export async function findByCriteria<T extends Model>(
  criteria: SearchCriteria[],
  model: ModelStatic<T>,
  addition: SearchAddition,
  includeType: AutoInclude | ManualInClude,
  transaction: Transaction
): Promise<T[] | GroupedData<T> | any> {
  const conditions: any[] = [];
  let includeOptions;
  if (includeType.option === 'auto') {
    includeOptions = await buildIncludeCriteria(
      criteria,
      addition,
      includeType.dbSource,
    );
  } else {
    includeOptions = includeType.includeOption;
  }
  criteria.forEach((criterion) => {
    const { field, operator, value } = criterion;

    const formattedField = field.includes('.')
      ? `$${field}$`
      : `$${model.name}.${field}$`;

    switch (operator) {
      case '~':
        // conditions.push({ [formattedField]: { [Op.like]: `%${value}%` } });
        conditions.push(
          Sequelize.where(
            fn('LOWER', col(formattedField.replace(/\$/g, ''))),
            {
              [Op.like]: `%${value.toLowerCase()}%`
            }
          )
        );
        break;
      case '!~':
        // conditions.push({ [formattedField]: { [Op.notLike]: `%${value}%` } });
        conditions.push(
          Sequelize.where(
            fn('LOWER', col(formattedField.replace(/\$/g, ''))),
            {
              [Op.notLike]: `%${value.toLowerCase()}%`
            }
          )
        );
        break;
      case '=':
        conditions.push({ [formattedField]: value });
        break;
      case '!=':
        conditions.push({ [formattedField]: { [Op.ne]: value } });
        break;
      case '<=':
        conditions.push({ [formattedField]: { [Op.lte]: value } });
        break;
      case '>=':
        conditions.push({ [formattedField]: { [Op.gte]: value } });
        break;
      case '<':
        conditions.push({ [formattedField]: { [Op.lt]: value } });
        break;
      case '>':
        conditions.push({ [formattedField]: { [Op.gt]: value } });
        break;
      case 'isSet':
        conditions.push({ [formattedField]: { [Op.not]: null } });
        break;
      case 'isNotSet':
        conditions.push({ [formattedField]: null });
        break;
      default:
        throw new Error(`Unknown operator: ${operator}`);
    }
  });

  const primaryKeyField = model.primaryKeyAttribute;
  let baseFindOptions: FindOptions<T> = {
    attributes: Object.keys(model.getAttributes()),
    include: includeOptions,
    where: {
      [Op.and]: conditions,
    }
  };
  if(transaction) {
    baseFindOptions.transaction = transaction;
  }
  

  if (addition) {
    if (addition.sort) {
      baseFindOptions.order = addition.sort.map((sortCriterion) => {
        const [field, direction] = sortCriterion;
        if (field.includes('.')) {
          const parts = field.split('.');
          const association = parts.slice(0, -1).join('.');
          const column = parts[parts.length - 1];
          // console.log(
          //   association,
          //   column,
          //   model.associations[association].target,
          // );
          return [
            { model: model.associations[association].target, as: association },
            column,
            direction,
          ];
        }
        return [field, direction];
      });
    }

    if (addition.page !== undefined && addition.size !== undefined) {
      baseFindOptions.limit = addition.size;
      baseFindOptions.offset = (addition.page - 1) * addition.size;
    }
  }

  const primaryKeys = await model.findAll(baseFindOptions);
  const primaryKeyValues = primaryKeys.map((item) => item[primaryKeyField]);

  if (primaryKeyValues.length === 0) {
    return [];
  }

  let findOptions: FindOptions = {
    where: {
      id: {
        [Op.in]: [...primaryKeyValues],
      }
    },
    include: includeOptions,
    subQuery: false
  };
  if(transaction) {
    findOptions.transaction = transaction;
  }
  
  const result = await model.findAll(findOptions);

  if (addition && addition.group) {
    return groupByRecursive(result, addition.group);
  }

  return result;
}

function groupByRecursive<T>(
  data: T[],
  groupByFields: string[],
  currentIndex: number = 0,
): GroupedData<T> | T[] {
  if (currentIndex >= groupByFields.length) {
    return data;
  }

  const currentField = groupByFields[currentIndex];
  const groupedData: GroupedData<T> = {};

  data.forEach((item) => {
    let groupKeys: any[] = [item[currentField]];

    if (currentField.includes('.')) {
      const nestedFields = currentField.split('.');
      let currentItem = item;
      groupKeys = [];
      for (const field of nestedFields) {
        if (currentItem && currentItem[field] !== undefined) {
          currentItem = currentItem[field];
        } else {
          currentItem = item[currentField];
          break;
        }
      }
      groupKeys = Array.isArray(currentItem) ? currentItem : [currentItem];
    } else if (Array.isArray(item[currentField])) {
      groupKeys = item[currentField];
    }

    groupKeys.forEach((groupKey) => {
      if (!groupedData[groupKey]) {
        groupedData[groupKey] = [item];
      } else {
        (groupedData[groupKey] as T[]).push(item);
      }
    });
  });

  const nextIndex = currentIndex + 1;
  for (const key in groupedData) {
    groupedData[key] = groupByRecursive(
      groupedData[key] as unknown as T[],
      groupByFields,
      nextIndex,
    );
  }

  return groupedData;
}

async function buildIncludeCriteria(
  criterias: SearchCriteria[],
  additions: SearchAddition,
  dbSource: Sequelize,
) {
  const modelSet = new Set<string>();
  const fields: string[] = additions.group ? [
    ...criterias.map((criteria) => criteria.field),
    ...additions.group,
    ...additions.sort.map((sort) => sort[0]),
  ] : [
    ...criterias.map((criteria) => criteria.field),
    ...additions.sort.map((sort) => sort[0]),
  ];
  
  const includeOptions: IncludeOptions[] = [];
  function addModel(field: string) {
    const relations: string[] = field.split('.');
    relations.pop();
    if (!relations) return;
    let currentModel: any;
    let prevInclude: IncludeOptions[] = includeOptions;
    relations.forEach((relation) => {
      relation = relation.charAt(0).toUpperCase() + relation.slice(1);
      if (!modelSet.has(relation)) {
        currentModel = {
          model: dbSource.models[relation],
          include: [],
        };
        prevInclude.push(currentModel);
        modelSet.add(relation);
      } else {
        currentModel = prevInclude.find(
          (includeModel: IncludeOptions) =>
            includeModel.model.name === relation,
        );
      }
      prevInclude = currentModel.include;
    });
  }
  fields.forEach((field) => {
    addModel(field);
  });
  return includeOptions;
}


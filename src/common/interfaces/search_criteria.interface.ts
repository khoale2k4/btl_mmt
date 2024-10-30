export interface SearchCriteria {
    field: string;
    operator: '~' | '!~' | '=' | '!=' | 'isSet' | 'isNotSet' | '<' | '<=' | '>' | '>=';
    value?: any;
}

import { SearchAddition } from "./search_addition.interface";
import { SearchCriteria } from "./search_criteria.interface";

export interface SearchPayload {
    criteria: SearchCriteria[],
    addition: SearchAddition
}
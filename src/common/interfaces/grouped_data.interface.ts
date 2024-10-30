export interface GroupedData<T> {
    [key: string]: T[] | GroupedData<T>;
}
export interface SearchAddition {
    sort: [string, 'ASC' | 'DESC'][],
    page: number,
    size: number,
    group: string[]
}
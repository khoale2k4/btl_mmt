export interface IDatabaseConfigAttributes {
  username?: string;
  password?: string;
  database?: string;
  host?: string;
  port?: number | string;
  dialect?: string;
  urlDatabase?: string;
  pool: {
    max: number;       // Kiểu số, xác định số lượng kết nối tối đa trong pool.
    min: number;       // Kiểu số, xác định số lượng kết nối tối thiểu trong pool.
    acquire: number;   // Kiểu số, xác định thời gian tối đa (tính bằng mili giây) để cố gắng lấy một kết nối trước khi bỏ cuộc.
    idle: number;      // Kiểu số, xác định thời gian tối đa (tính bằng mili giây) mà một kết nối có thể ở trạng thái không hoạt động trước khi bị giải phóng.
  }
}
export interface IDatabaseConfig {
  development: IDatabaseConfigAttributes;
  test: IDatabaseConfigAttributes;
  production: IDatabaseConfigAttributes;
}

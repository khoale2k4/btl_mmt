import * as dotenv from 'dotenv';
import { IDatabaseConfig } from './interfaces/dbConfig.interface';

dotenv.config();

export const databaseConfig: IDatabaseConfig = {
  development: {
    username: process.env.DB_USER,
    password: process.env.DB_PASS,
    database: process.env.DB_NAME_DEVELOPMENT,
    host: process.env.DB_HOST,
    port: Number(process.env.DB_PORT),
    dialect: process.env.DB_DIALECT as 'mariadb' | 'mysql',
    pool: {
      max: 10,          // Maximum number of connections in pool
      min: 0,           // Minimum number of connections in pool
      acquire: 30000,   // Max time (ms) pool will try to get connection before throwing error
      idle: 10000,      // Max time (ms) that a connection can be idle before being released
    }
  },
  test: {
    username: process.env.DB_USER,
    password: process.env.DB_PASS,
    database: process.env.DB_NAME_TEST,
    host: process.env.DB_HOST,
    port: process.env.DB_PORT,
    dialect: process.env.DB_DIALECT,
    pool: {
      max: 5,
      min: 0,
      acquire: 10000,
      idle: 5000,
    },
  },
  production: {
    username: process.env.DB_USER,
    password: process.env.DB_PASS,
    database: process.env.DB_NAME_PRODUCTION,
    host: process.env.DB_HOST,
    port: Number(process.env.DB_PORT),
    dialect: process.env.DB_DIALECT as 'mariadb' | 'mysql',
    pool: {
      max: 20,         // Adjust based on your application's needs
      min: 5,
      acquire: 30000,  // Production environments can typically handle longer acquire times
      idle: 10000,
    },
  },
};

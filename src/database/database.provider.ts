import { DEVELOPMENT, PRODUCTION, SEQUELIZE, TEST } from "src/common/contants";
import { databaseConfig } from "./database.config";
import { Sequelize } from "sequelize-typescript";
import { Peer } from "src/modules/peer/entities/peer.entity";
import { PeerHoldFile } from "src/modules/peer/entities/peer_hold_file.entity";
import { File } from "src/modules/file/entities/file.entity";
import { User } from "src/modules/users/entities/user.entity";


export const databaseProviders = [
  {
    provide: SEQUELIZE,
    useFactory: async () => {
      let config;
      switch (process.env.NODE_ENV) {
        case DEVELOPMENT:
          config = databaseConfig.development;
          break;
        case TEST:
          config = databaseConfig.test;
          break;
        case PRODUCTION:
          config = databaseConfig.production;
          break;
        default:
          config = databaseConfig.development;
      }
      const sequelize = new Sequelize(config);
      sequelize.addModels([Peer, PeerHoldFile, File, User]);
      await sequelize.sync();

      try {
        await sequelize.authenticate();
        console.log('Connection has been established successfully');
        await sequelize.sync();
        console.log('Database synchronized successfully');
      } catch (error) {
        console.error('Unable to connect to the database:', error);
      }
      
      return sequelize;
    },
  },
];

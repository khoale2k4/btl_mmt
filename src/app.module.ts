import { Module } from '@nestjs/common';
import { AppController } from './app.controller';
import { AppService } from './app.service';
import { DatabaseModule } from './database/database.module';
import { PeerModule } from './modules/peer/peer.module';
import { FileModule } from './modules/file/file.module';
import { UserModule } from './modules/users/user.module';

@Module({
  imports: [DatabaseModule, PeerModule, FileModule, UserModule],
  controllers: [AppController],
  providers: [AppService],
})
export class AppModule {}

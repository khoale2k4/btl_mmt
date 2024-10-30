import { Module } from "@nestjs/common";
import { PeerModule } from "../peer/peer.module";
import { filesProviders } from "./file.provider";
import { FileService } from "./services/file.service";
import { PeerHoldFileService } from "../peer/services/peer_hold_file.service";
import { FileController } from "./controllers/file.controller";
import { UserModule } from "../users/user.module";
import { UserService } from "../users/services/user.service";
import { LoggerModule } from "src/common/logger/logger.module";
import { ResponseModule } from "../response/response.module";



@Module({
    imports: [FileModule, PeerModule, PeerModule, UserModule, LoggerModule, ResponseModule],
    providers: [...filesProviders, FileService, PeerHoldFileService, UserService],
    controllers: [FileController],
    exports: [...filesProviders, FileService, PeerHoldFileService, UserService]
})
export class FileModule {}
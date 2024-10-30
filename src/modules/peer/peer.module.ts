import { DatabaseModule } from "src/database/database.module";
import { PeerService } from "./services/peer.service";
import { Module } from "@nestjs/common";
import { peerProviders } from "./peer.provider";
import { LoggerModule } from "src/common/logger/logger.module";
import { ResponseModule } from "../response/response.module";
import { PeerHoldFileService } from "./services/peer_hold_file.service";


@Module({
    imports: [
        DatabaseModule,
        LoggerModule,
        ResponseModule
    ],
    controllers: [],
    providers: [...peerProviders, PeerService, PeerHoldFileService],
    exports: [PeerService, PeerHoldFileService]
})
export class PeerModule {}
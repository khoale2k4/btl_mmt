import { FILE_REPOSITORY, PEER_HOLD_FILE_REPOSITORY, PEER_REPOSITORY } from "src/common/contants";
import { File } from "./entities/file.entity";
import { Peer } from "../peer/entities/peer.entity";
import { PeerHoldFile } from "../peer/entities/peer_hold_file.entity";

export const filesProviders = [{
    provide: FILE_REPOSITORY,
    useValue: File
}, {
    provide: PEER_REPOSITORY,
    useValue: Peer
}, {
    provide: PEER_HOLD_FILE_REPOSITORY,
    useValue: PeerHoldFile
}]
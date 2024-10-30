import { PEER_HOLD_FILE_REPOSITORY, PEER_REPOSITORY} from "src/common/contants";
import { Peer } from "./entities/peer.entity";
import { PeerHoldFile } from "./entities/peer_hold_file.entity";


export const peerProviders = [{
    provide: PEER_REPOSITORY,
    useValue: Peer
}, {
    provide: PEER_HOLD_FILE_REPOSITORY,
    useValue: PeerHoldFile,
}]
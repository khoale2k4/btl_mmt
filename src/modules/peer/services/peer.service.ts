import { Inject, Injectable } from "@nestjs/common";
import { PEER_HOLD_FILE_REPOSITORY, PEER_REPOSITORY } from "src/common/contants";
import { Peer } from "../entities/peer.entity";
import { CreatePeerDto } from "../dtos/create-peer.dtos";
import { PeerHoldFile } from "../entities/peer_hold_file.entity";


@Injectable()
export class PeerService {
    constructor(
        @Inject(PEER_REPOSITORY) private readonly peerRepository: typeof Peer
    ) {};

    async create(peer: CreatePeerDto) {
        return await this.peerRepository.create({
            IPaddress: peer.IPaddress,
            port: peer.port
        });
    }

    async findByAddressAndPort(IPaddress: string, port: number) {
        return await this.peerRepository.findOne({
            where: {
                IPaddress,
                port
            }
        });
    }
}
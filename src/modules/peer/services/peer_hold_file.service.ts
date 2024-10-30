import { ConflictException, Inject, Injectable } from "@nestjs/common";
import { PEER_HOLD_FILE_REPOSITORY, PEER_REPOSITORY } from "src/common/contants";
import { Peer } from "../entities/peer.entity";
import { PeerHoldFile } from "../entities/peer_hold_file.entity";
import { CreatePHFDTO } from "../dtos/create-phf.dtos";


@Injectable()
export class PeerHoldFileService {
    constructor(
        @Inject(PEER_REPOSITORY) private readonly peerRepository: typeof Peer,
        @Inject(PEER_HOLD_FILE_REPOSITORY) private readonly pHFRepository: typeof PeerHoldFile
    ){};


    async create(createDto: CreatePHFDTO) {
        const existedRelation = await this.pHFRepository.findOne({
            where: {
                fileId: createDto.fileId,
                peerId: createDto.peerId
            }
        });

        if(existedRelation) {
            throw new ConflictException('Liên kết Peer-File đã được tạo từ trước');
        }

        return await this.pHFRepository.create({
            fileId: createDto.fileId,
            peerId: createDto.peerId 
        });
    }

}
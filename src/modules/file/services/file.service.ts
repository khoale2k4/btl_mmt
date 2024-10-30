import { BadRequestException, Inject, Injectable, NotFoundException } from "@nestjs/common";
import { FILE_REPOSITORY, PEER_HOLD_FILE_REPOSITORY, PEER_REPOSITORY } from "src/common/contants";
import { File } from "../entities/file.entity";
import { Peer } from "src/modules/peer/entities/peer.entity";
import { PeerHoldFile } from "src/modules/peer/entities/peer_hold_file.entity";
import { UserService } from "src/modules/users/services/user.service";
import { PeerService } from "src/modules/peer/services/peer.service";
import { PeerHoldFileService } from "src/modules/peer/services/peer_hold_file.service";
import { FindOptions } from "sequelize";
import { User } from "src/modules/users/entities/user.entity";
import { UUID } from "crypto";
import { UploadFileDto } from "../dtos/upload-file.dto";
import { CreatePeerHoldFileDto } from "../dtos/create-peer-hold-file.dto";



@Injectable()
export class FileService {
    constructor(
        @Inject(FILE_REPOSITORY) private readonly fileRepository: typeof File,
        @Inject(PEER_REPOSITORY) private readonly peerRepository: typeof Peer,
        @Inject(PEER_HOLD_FILE_REPOSITORY) private readonly pHFRepository: typeof PeerHoldFile,
        private readonly userService: UserService,
        private readonly peerService: PeerService,
        private readonly pHFService: PeerHoldFileService
    ) {}

    async search(infoHash: string) {

        let findOption: FindOptions = {
            include: [
                { 
                    model: Peer, 
                    through: { attributes: [] }, 
                    attributes: ['IPaddress', 'port']
                },
                { 
                    model: User,
                    attributes: ['fullname']
                }
            ]
        };

        if (infoHash) {
            findOption.where = { infoHash };
        }

        return await this.fileRepository.findAll(findOption);
    }

    async create(dto: UploadFileDto) {
        const existedUser = await this.userService.findOneById(dto.userId);
        if (!existedUser) {
            throw new NotFoundException('Người dùng không tồn tại');
        }
        
        const [file] = await this.fileRepository.findOrCreate({
            where: {
                infoHash: dto.infoHash
            },
            defaults: {
                infoHash: dto.infoHash,
                name: dto.filename,
                size: dto.size,
                userId: dto.userId
            }
        });
             
        const [peer] = await this.peerRepository.findOrCreate({
            where: {
                IPaddress: dto.peerIPAddress,
                port: dto.peerPort
            },

            defaults: {
                IPaddress: dto.peerIPAddress,
                port: dto.peerPort
            }
        })

        await this.pHFService.create({ fileId: file.id, peerId: peer.id });
        return file;
    }

    async createPHF(createPeerHoldFileDto: CreatePeerHoldFileDto) {
        
        const { infoHash, peerAddress, peerPort, fileName, fileSize } = createPeerHoldFileDto;

        const [peer] = await this.peerRepository.findOrCreate({
            where: {
                IPaddress: peerAddress,
                port: peerPort
            },

            defaults: {
                IPaddress: peerAddress,
                port: peerPort
            }
        });

        let existedFile = await this.fileRepository.findOne({
            where: {
                infoHash: infoHash
            }
        });

        if (!existedFile) {
            existedFile = await this.fileRepository.create({
                infoHash: infoHash,
                name: fileName,
                size: fileSize
            });
        }


        const [file] = await this.fileRepository.findOrCreate({
            where: {
                infoHash
            },

            defaults: {
                infoHash,
                name: fileName,
                size: fileSize
            }
        });

        const [peerHoldFile, created] = await this.pHFRepository.findOrCreate({
            where: {
                fileId: file.id,
                peerId: peer.id
            },

            defaults: {
                fileId: file.id,
                peerId: peer.id
            }
        });

        if(!created) {
            throw new BadRequestException('Bạn đã upload file này từ trước');
        }
         
        return peerHoldFile;
    }


}
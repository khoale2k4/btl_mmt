import { UUID } from "crypto";

export class UploadFileDto {
    infoHash: string;
    filename: string;
    peerIPAddress: string;
    peerPort: number;
    size: number;
    userId: UUID;
}
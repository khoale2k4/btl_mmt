export class CreatePeerHoldFileDto {
    infoHash: string;
    fileName: string;
    fileSize: number;
    peerAddress: string;
    peerPort: number;
}
// import { BadRequestException, Body, Controller, HttpStatus, InternalServerErrorException, Post, Req, Res } from "@nestjs/common";
// import { Response } from "src/modules/response/response.entity";
// import { PeerService } from "../services/peer.service";
// import { CreatePeerDto } from "../dtos/create-peer.dtos";
// import { LoggerService } from "src/common/logger/logger.service";


// @Controller('peer')
// export class PeerController {
//     constructor(
//         private readonly peerService: PeerService,
//         private readonly logger: LoggerService,
//         private readonly response: Response
//     ) {}


//     @Post('create')
//     async create(
//         @Req() req,
//         @Body() dto: CreatePeerDto,
//         @Res() res
//     ) {
//         try { 
//             // const createdPeer = await this.
//             this.response.initResponse(true, "Tạo peer thành công", null);
//             return res.status(HttpStatus.CREATED).json(this.response);
//         } catch (error) {
// 			this.logger.error(error.message, error.stack);
// 			if (error instanceof InternalServerErrorException) {
// 				this.response.initResponse(false, error.message, null);
// 				return res.status(HttpStatus.INTERNAL_SERVER_ERROR).json(this.response);
// 			}

// 			if (error instanceof BadRequestException) {
// 				this.response.initResponse(false, error.message, null);
// 				return res.status(HttpStatus.BAD_REQUEST).json(this.response);
// 			}

//             this.response.initResponse(false, "Đã xảy ra lỗi. Vui lòng thử lại", null);
// 			return res.status(HttpStatus.INTERNAL_SERVER_ERROR).json(this.response);
// 		}
//     }
// }
import { BadRequestException, Body, Controller, Get, HttpStatus, InternalServerErrorException, Post, Query, Req, Res } from "@nestjs/common";
import { FileService } from "../services/file.service";
import { LoggerService } from "src/common/logger/logger.service";
import { Response } from "src/modules/response/response.entity";
import { UploadFileDto } from "../dtos/upload-file.dto";
import { CreatePeerHoldFileDto } from "../dtos/create-peer-hold-file.dto";


@Controller()
export class FileController {
    constructor(
        private readonly fileService: FileService,
        private readonly logger: LoggerService,
        private readonly response: Response
    ) {}


    @Get('fetch') 
    async fetch(@Res() res, @Query('infoHash') infoHash: string) {
        try { 
            const file = await this.fileService.search(infoHash);
            this.response.initResponse(true, "Tạo peer thành công", file);
            return res.status(HttpStatus.CREATED).json(this.response);
        } catch (error) {
			this.logger.error(error.message, error.stack);
			if (error instanceof InternalServerErrorException) {
				this.response.initResponse(false, error.message, null);
				return res.status(HttpStatus.INTERNAL_SERVER_ERROR).json(this.response);
			}

			if (error instanceof BadRequestException) {
				this.response.initResponse(false, error.message, null);
				return res.status(HttpStatus.BAD_REQUEST).json(this.response);
			}

            this.response.initResponse(false, "Đã xảy ra lỗi. Vui lòng thử lại", null);
			return res.status(HttpStatus.INTERNAL_SERVER_ERROR).json(this.response);
		}
    }


    @Post('upload') 
    async upload(@Req() req, @Body() uploadFileDto: UploadFileDto, @Res() res) {
        try { 
            const createdFile = await this.fileService.create(uploadFileDto);
            this.response.initResponse(true, "Tạo peer thành công", createdFile);
            return res.status(HttpStatus.CREATED).json(this.response);
        } catch (error) {
			this.logger.error(error.message, error.stack);
			if (error instanceof InternalServerErrorException) {
				this.response.initResponse(false, error.message, null);
				return res.status(HttpStatus.INTERNAL_SERVER_ERROR).json(this.response);
			}

			if (error instanceof BadRequestException) {
				this.response.initResponse(false, error.message, null);
				return res.status(HttpStatus.BAD_REQUEST).json(this.response);
			}

            this.response.initResponse(false, "Đã xảy ra lỗi. Vui lòng thử lại", null);
			return res.status(HttpStatus.INTERNAL_SERVER_ERROR).json(this.response);
		}
    }


    @Post('/peer/hold') 
    async createPeerHoldFile(@Req() req, @Body() createPeerHoldFileDto: CreatePeerHoldFileDto, @Res() res) {
        try { 
            const createdPHF = await this.fileService.createPHF(createPeerHoldFileDto);
            this.response.initResponse(true, "Tạo peer thành công", createdPHF);
            return res.status(HttpStatus.CREATED).json(this.response);
        } catch (error) {
			this.logger.error(error.message, error.stack);
			if (error instanceof InternalServerErrorException) {
				this.response.initResponse(false, error.message, null);
				return res.status(HttpStatus.INTERNAL_SERVER_ERROR).json(this.response);
			}

			if (error instanceof BadRequestException) {
				this.response.initResponse(false, error.message, null);
				return res.status(HttpStatus.BAD_REQUEST).json(this.response);
			}

            this.response.initResponse(false, "Đã xảy ra lỗi. Vui lòng thử lại", null);
			return res.status(HttpStatus.INTERNAL_SERVER_ERROR).json(this.response);
		}
    }
}
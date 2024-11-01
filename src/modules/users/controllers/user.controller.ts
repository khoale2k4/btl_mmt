import { BadRequestException, Body, Controller, Get, HttpStatus, Param, Post, Res } from "@nestjs/common";
import { SignupDto } from "../dtos/signup.dto";

import { Response } from "src/modules/response/response.entity";
import { UserService } from "../services/user.service";
import { loginDto } from "../dtos/login.dto";
import { UUID } from "crypto";
import { FindOne } from "../dtos/find-one.dto";
import { UpdateDto } from "../dtos/update.dto";



@Controller('user')
export class UserController {
    constructor(
        private readonly userService: UserService,
        private readonly response: Response
    ) {};

    @Post('signup')
    async signUp(@Body() payload: SignupDto, @Res() res) {
        try {
            
            const createdUser = await this.userService.signup(payload);
            this.response.initResponse(true, 'Sign up successfully', createdUser);
            return res.status(HttpStatus.CREATED).json(this.response);
        } catch (error) {
            if (error instanceof BadRequestException) {
                this.response.initResponse(false, error.message, null);
                return res.status(HttpStatus.BAD_REQUEST).json(this.response);
            }

            console.log(error);
            this.response.initResponse(false, "Đã xảy ra lỗi. Vui lòng thử lại", null);
            return res.status(HttpStatus.INTERNAL_SERVER_ERROR).json(this.response);
        }
    }

    @Post('login')
    async login(@Body() payload: loginDto, @Res() res) {
        try {
            
            const loginResult = await this.userService.login(payload);
            this.response.initResponse(true, 'Login successfully', loginResult);
            return res.status(HttpStatus.CREATED).json(this.response);
        } catch (error) {
            if (error instanceof BadRequestException) {
                this.response.initResponse(false, error.message, null);
                return res.status(HttpStatus.BAD_REQUEST).json(this.response);
            }

            console.log(error);
            this.response.initResponse(false, "Đã xảy ra lỗi. Vui lòng thử lại", null);
            return res.status(HttpStatus.INTERNAL_SERVER_ERROR).json(this.response);
        }
    }


    @Get('/:id')
    async findOne(@Param('id') id: UUID, @Res() res) {
        try {
            console.log(id)
            const reuslt = await this.userService.findOneById(id);
            console.log(reuslt)
            this.response.initResponse(true, 'Get successfully', reuslt);
            return res.status(HttpStatus.CREATED).json(this.response);
        } catch (error) {
            if (error instanceof BadRequestException) {
                this.response.initResponse(false, error.message, null);
                return res.status(HttpStatus.BAD_REQUEST).json(this.response);
            }

            console.log(error);
            this.response.initResponse(false, "Đã xảy ra lỗi. Vui lòng thử lại", null);
            return res.status(HttpStatus.INTERNAL_SERVER_ERROR).json(this.response);
        }
    }


    @Get('/:id')
    async updateOne(@Param('id') id: UUID, @Body() payload: UpdateDto, @Res() res) {
        try {
            console.log(id)
            const result = await this.userService.updateOneById(payload, id);
            console.log(result)
            this.response.initResponse(true, 'Update successfully', result);
            return res.status(HttpStatus.CREATED).json(this.response);
        } catch (error) {
            if (error instanceof BadRequestException) {
                this.response.initResponse(false, error.message, null);
                return res.status(HttpStatus.BAD_REQUEST).json(this.response);
            }

            console.log(error);
            this.response.initResponse(false, "Đã xảy ra lỗi. Vui lòng thử lại", null);
            return res.status(HttpStatus.INTERNAL_SERVER_ERROR).json(this.response);
        }
    }

}
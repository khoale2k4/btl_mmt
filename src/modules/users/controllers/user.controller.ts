import { BadRequestException, Body, Controller, HttpStatus, Post, Res } from "@nestjs/common";
import { SignupDto } from "../dtos/signup.dto";

import { Response } from "src/modules/response/response.entity";
import { UserService } from "../services/user.service";
import { loginDto } from "../dtos/login.dto";



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

}
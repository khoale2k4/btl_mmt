import { BadRequestException, Inject, Injectable, UnauthorizedException } from "@nestjs/common";
import { USER_REPOSITORY } from "src/common/contants";
import { User } from "../entities/user.entity";
import { SignupDto } from "../dtos/signup.dto";
import * as bcrypt from 'bcrypt';
import { loginDto } from "../dtos/login.dto";
import { UUID } from "crypto";
import { UpdateDto } from "../dtos/update.dto";

@Injectable()
export class UserService {
    constructor(
        @Inject(USER_REPOSITORY) private readonly userRepository: typeof User
    ) {}

    async signup(createUserDto: SignupDto) {
        const existedUser = await this.userRepository.findOne({
            where: {
                username: createUserDto.username
            }
        });

        if(existedUser) {
            throw new BadRequestException('Tài khoản đã tồn tại');
        }

        const hashPassword = await bcrypt.hash(createUserDto.password, 5);
        return await this.userRepository.create({
            username: createUserDto.username,
            password: hashPassword,
            fullName: createUserDto.fullname
        });
    }


    async login(loginDto: loginDto) {
        const existedUser = await this.userRepository.findOne({
            where: {
                username: loginDto.username
            }
        });

        if(!existedUser) {
            throw new BadRequestException('Người dùng không tồn tại');
        }

        const passWordMatching = await bcrypt.compare(loginDto.password, existedUser.password);
        if(!passWordMatching) {
            throw new UnauthorizedException('Mật khẩu không đúng');
        }

        const { password, ...userWithoutPassword } = existedUser['dataValues'];
        return userWithoutPassword;
    }

    async findOneById(id: UUID) {
        return await this.userRepository.findByPk(id);
    }

    async updateOneById(payload: UpdateDto, id: UUID) {
        return this.userRepository.update(payload, {
            where: {
                id
            }
        });
    }
    
}
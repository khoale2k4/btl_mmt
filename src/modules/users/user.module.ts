import { Module } from "@nestjs/common";
import { DatabaseModule } from "src/database/database.module";
import { ResponseModule } from "../response/response.module";
import { userProviders } from "./user.provider";
import { UserService } from "./services/user.service";
import { UserController } from "./controllers/user.controller";



@Module({
    imports: [
        DatabaseModule,
        ResponseModule
    ],
    providers: [
        ...userProviders,
        UserService,
    ],
    controllers: [UserController],
    exports: [UserService, ...userProviders],
})
export class UserModule {}
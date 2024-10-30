import { validate, ValidationError } from 'class-validator';
import { plainToClass } from 'class-transformer';
import { BadRequestException } from '@nestjs/common';

// Hàm chung để xác thực DTO
export async function validateDto<T extends object>(dtoClass: new () => T, dto: Partial<T>) {
    const instance = plainToClass(dtoClass, dto);
    const errors = await validate(instance);
    if (errors.length > 0) {
        const firstError = errors[0];
        const errorMessages = Object.values(firstError.constraints || {});
        throw new BadRequestException(errorMessages.join(', '));
    }
}

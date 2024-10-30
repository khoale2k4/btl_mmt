import { Injectable, Logger, Scope } from '@nestjs/common';

@Injectable({ scope: Scope.TRANSIENT })
export class LoggerService {
  private readonly logger = new Logger(LoggerService.name);

  private formatMessage(level: string, message: string): string {
    const now = new Date();
    const hour = `${this.pad(now.getHours())}:${this.pad(now.getMinutes())}:${this.pad(now.getSeconds())}`
    const day = `${this.pad(now.getDate())}/${this.pad(now.getMonth() + 1)}/${now.getFullYear()}`;
    const time = hour + ' ' + day;
    return `[${time}] [${level}] ${message}`;
  }

  private pad(number: number): string {
    return number < 10 ? `0${number}` : `${number}`;
  }

  error(message: string, trace: string) {
    this.logger.error(this.formatMessage('ERROR', message), trace);
  }

  warn(message: string) {
    this.logger.warn(this.formatMessage('WARN', message));
  }

  debug(message: string) {
    this.logger.debug(this.formatMessage('DEBUG', message));
  }

  verbose(message: string) {
    this.logger.verbose(this.formatMessage('VERBOSE', message));
  }

  fatal(message: string) {
    this.logger.error(this.formatMessage('FATAL', message));
  }
}

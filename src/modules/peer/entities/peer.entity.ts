
import { UUID } from 'crypto';
import { UUIDV4 } from 'sequelize';
import {
    Table,
    Column,
    Model,
    DataType,
    PrimaryKey,
    Default,
    AllowNull,
    HasMany,
    Unique,
    ForeignKey,
    BelongsTo,
    BelongsToMany,
} from 'sequelize-typescript';
import { PeerHoldFile } from './peer_hold_file.entity';
import { File } from 'src/modules/file/entities/file.entity';


@Table
export class Peer extends Model<Peer> {
    @PrimaryKey
    @Default(UUIDV4)
    @AllowNull(false)
    @Column(DataType.UUID)
    id: UUID;

    @Column(DataType.STRING)
    IPaddress: string;

    @Column(DataType.INTEGER)
    port: number;

    @BelongsToMany(()=> File, () => PeerHoldFile)
    files: File[];
}
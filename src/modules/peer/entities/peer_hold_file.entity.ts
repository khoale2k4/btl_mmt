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
} from 'sequelize-typescript';
import { File } from 'src/modules/file/entities/file.entity';
import { Peer } from './peer.entity';


@Table
export class PeerHoldFile extends Model<PeerHoldFile> {
    @PrimaryKey
    @Default(UUIDV4)
    @AllowNull(false)
    @Column(DataType.UUID)
    id: UUID;

    @ForeignKey(() => File)
    @Column(DataType.UUID)
    fileId: UUID;
  
    @ForeignKey(() => Peer)
    @Column(DataType.UUID)
    peerId: UUID
}
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
import { Peer } from 'src/modules/peer/entities/peer.entity';
import { PeerHoldFile } from 'src/modules/peer/entities/peer_hold_file.entity';
import { User } from 'src/modules/users/entities/user.entity';


@Table
export class File extends Model<File> {
    @PrimaryKey
    @Default(UUIDV4)
    @Column(DataType.UUID)
    id: UUID;
    
    @Column(DataType.STRING)
    name: string;

    @Column(DataType.INTEGER)
    size: number;

    @Unique
    @Column(DataType.STRING(255)) // or another suitable length for your data
    infoHash: string;

    @ForeignKey(() => User)
    @Column(DataType.UUID)
    userId: UUID;

    @BelongsTo(() => User)
    user: User;

    @BelongsToMany(() => Peer, () => PeerHoldFile)
    peers: Peer[];

}
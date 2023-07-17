import { Video} from './domains/Video';
import IVideoCatalog from './interfaces/IVideoCatalog';
import Catalog from '../../common/catalogs/Catalog';
import { VideoBasic } from './domains/VideoBasic';
import { VideoInfo } from './domains/VideoInfo';

export default class VideoCatalog extends Catalog implements IVideoCatalog {

    async getByIDVideoInfo(id: number): Promise<VideoInfo> {
        const sql = `
            select v.ID, v.title, v.video_name, v.climber_id, c.\`name\` as climber_name, v.\`date\`, v.attempt, v.\`url\`, v.\`start\`, v.\`end\`, v.\`time\`, v.frames, v.side
            from video AS v
            inner join climber AS c on v.climber_id = c.ID
            WHERE v.ID = ?
            order by v.ID asc;
        `.replace(/\s+|\n/g, ' ')

        return this._getOneInfo(this._toVideosInfo(await Catalog.getConnector().query({ query: sql, bindings: [id] })));
    }
    
    async getAllBasic(): Promise<VideoBasic[]> {
        const sql = `
            select video.ID, video.title, video.video_name, climber.\`name\` as climber_name, video.climber_id, video.\`date\`, video.attempt, video.\`time\`
            from video
            inner join climber on video.climber_id = climber.ID
            order by video.ID asc;
        `.replace(/\s+|\n/g, ' ')

        return this._toVideosBasic(await Catalog.getConnector().query({ query: sql }));
    }

    async getByID(id: number): Promise<Video> {
        const sql = `
            SELECT *
            FROM video 
            WHERE ID = ?;
        `.replace(/\s+|\n/g, ' ')

        return this._getOne(this._toVideos(await Catalog.getConnector().query({ query: sql, bindings: [id] })));
    }

    async getAll(): Promise<Video[]> { // add option to return climber name
        const sql = `
            select v.ID, v.title, v.video_name, v.climber_id, c.\`name\` as climber_name, v.\`date\`, v.attempt, v.\`url\`, v.\`start\`, v.\`end\`, v.\`time\`, v.frames, v.side, v.skeletons, v.trans_matrixes
            from video AS v
            inner join climber AS c on v.climber_id = c.ID
            order by v.ID asc;
        `.replace(/\s+|\n/g, ' ')

        return this._toVideos(await Catalog.getConnector().query({ query: sql }));
    }

    async getAllDates(): Promise<string[]> {
        const sql = `
            select distinct \`date\`
            from video;
        `.replace(/\s+|\n/g, ' ')

        return this._toString(await Catalog.getConnector().query({ query: sql }));
    }

    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    private _toVideos(result: any): Video[] {
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        return result.map((video: any) => video);
    }

    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    private _toVideosBasic(result: any): VideoBasic[] {
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        return result.map((videoBasic: any) => videoBasic);
    }

    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    private _toVideosInfo(result: any): VideoInfo[] {
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        return result.map((video: any) => video);
    }

    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    private _toString(result: any): string[] {
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        return result.map((value: any) => value);
    }

    private _getOne(videos: Video[]): Video {
        if (!videos.length) {
            throw new Error('Video not found!')
        }

        return videos[0];

    }

    private _getOneInfo(videos: VideoInfo[]): VideoInfo {
        if (!videos.length) {
            throw new Error('Video not found!')
        }

        return videos[0];

    }

}
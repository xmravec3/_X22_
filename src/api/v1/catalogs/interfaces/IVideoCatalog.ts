import { Video } from '../domains/Video';
import { VideoBasic } from '../domains/VideoBasic';
import { VideoInfo } from '../domains/VideoInfo';

export default interface IVideoCatalog {

    getByID(id: number): Promise<Video>
    getAll(): Promise<Video[]>

    getAllBasic(): Promise<VideoBasic[]>

    getByIDVideoInfo(id: number): Promise<VideoInfo>

    getAllDates(): Promise<string[]>

}
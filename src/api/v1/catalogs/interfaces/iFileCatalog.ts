import { File } from '../domains/File';

export default interface IFileCatalog {

    getByID(id: number): Promise<File>
    
}
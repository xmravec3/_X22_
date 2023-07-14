import Catalog from '../../common/catalogs/Catalog';
import { File } from './domains/File';
import IFileCatalog from './interfaces/iFileCatalog';

export default class FileCatalog extends Catalog implements IFileCatalog {
    getByID(id: number): Promise<File> {
        throw new Error('Method not implemented.');
    }


}
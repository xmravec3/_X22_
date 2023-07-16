import { Climber} from './domains/Climber';
import IClimberCatalog from './interfaces/IClimberCatalog';
import Catalog from '../../common/catalogs/Catalog';

export default class ClimberCatalog extends Catalog implements IClimberCatalog {

    async getByID(id: number): Promise<Climber> {
        const sql = `
            SELECT *
            FROM climber 
            WHERE ID = ?;
        `.replace(/\s+|\n/g, ' ')

        return this._getOne(this._toClimbers(await Catalog.getConnector().query({ query: sql, bindings: [id] })));
    }

    async getAll(): Promise<Climber[]> {
        const sql = `
            SELECT *
            FROM climber 
            ORDER BY ID ASC;
        `.replace(/\s+|\n/g, ' ')

        return this._toClimbers(await Catalog.getConnector().query({ query: sql }));
    }

    async getAllWithVideo(): Promise<Climber[]> {
        const sql = `
            select distinct v.climber_id as ID, c.\`name\` as name
            from video AS v
            inner join climber AS c on v.climber_id = c.ID;
        `.replace(/\s+|\n/g, ' ')

        return this._toClimbers(await Catalog.getConnector().query({ query: sql }));
    }

    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    private _toClimbers(result: any): Climber[] {
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        return result.map((climber: any) => climber);
    }

    private _getOne(climbers: Climber[]): Climber {
        if (!climbers.length) {
            throw new Error('Climber not found!')
        }

        return climbers[0];

    }

}
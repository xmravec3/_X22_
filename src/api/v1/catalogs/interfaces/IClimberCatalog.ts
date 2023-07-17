import { Climber } from '../domains/Climber';

export default interface IClimberCatalog {

    getByID(id: number): Promise<Climber>

    getAll(): Promise<Climber[]>

    getAllWithVideo(): Promise<Climber[]>
    
}
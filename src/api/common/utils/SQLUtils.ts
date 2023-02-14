export default class SQLUtils<Field extends string> {

    buildProjection(configuration: Record<Field, string[]>, fields?: Field[]): string {
        if (!Array.isArray(fields) || !fields.length) {
            return Object.values(configuration).flat().join(', ');
        }

        const projection = Object.entries(configuration)
            .filter(([key]) => fields.includes(key as Field))
            .map(([, value]) => value)
            .flat()

        if (projection.length) {
            return projection.join(', ')
        }

        return Object.values(configuration).flat().join(', ');
    }

}
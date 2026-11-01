from sqlalchemy import inspect
from app.core.db_init import engine


def get_schema_description() -> str:
    inspector = inspect(engine)
    lines = []

    for table_name in inspector.get_table_names():
        lines.append(f"Table: {table_name}")

        columns = inspector.get_columns(table_name)
        for col in columns:
            line = f"  - {col['name']} ({col['type']})"
            if not col.get("nullable", True):
                line += " NOT NULL"
            lines.append(line)

        fks = inspector.get_foreign_keys(table_name)
        for fk in fks:
            local_cols = ", ".join(fk['constrained_columns'])
            ref_table = fk['referred_table']
            ref_cols = ", ".join(fk['referred_columns'])
            lines.append(
                f"  - FOREIGN KEY ({local_cols}) REFERENCES {ref_table}({ref_cols})"
            )

        lines.append("")

    return "\n".join(lines)


if __name__ == "__main__":
    print(get_schema_description())
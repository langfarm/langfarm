import unittest

import sqlalchemy

from langfarm_tests.base_for_test import get_test_logger
from langfarm_tests.langfuse_container import LangfuseDBContainerTestCase

logger = get_test_logger(__name__)


class InitLangfuseDBTestCase(LangfuseDBContainerTestCase):
    def test_assert_init(self):
        table_id_map = {
            "users": "cm6g082zk000013r2t86dhtib",
            "organizations": "cm6g0t2nu000113r2msztoha4",
            "organization_memberships": "cm6ok6abq0005x2j8vd9xlx4d",
            "projects": "cm6g0uptx000613r2ha6hxtkc",
            "api_keys": "cm6g0uzgj000913r25shr4z98",
        }
        models = [
            "cm3azlpbl000o3rpmuhabmi9y",
            "cm3azj5o6000g3rpmnd4llx6f",
            "cm3azj5o6000g3rpmxb3iiu8g",
            "cm3b047f2000w3rpmdnv0bxpb",
        ]

        with self.get_db_engine().begin() as conn:
            for k, v in table_id_map.items():
                result = conn.execute(sqlalchemy.text(f"select id from {k}"))
                row = result.first()
                if row:
                    _id = row[0]
                    logger.info("select id from %s, result=%s", k, _id)
                    assert _id == v
                else:
                    assert False

            # assert models
            for m in models:
                result = conn.execute(sqlalchemy.text(f"select id from models where id='{m}'"))
                row = result.first()
                if row:
                    _id = row[0]
                    logger.info("select id from models where id='%s', result=%s", m, _id)
                    assert _id == m
                else:
                    assert False


if __name__ == "__main__":
    unittest.main()

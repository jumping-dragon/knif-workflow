import datetime

import psycopg
from psycopg.rows import class_row
from psycopg.types.json import Jsonb

from .config import CONN_STR, SCHEMA
from .model import Ioc, Page, PageStatus, Relation

Connection = psycopg.connect(CONN_STR, options=f"-c search_path={SCHEMA}")


def add_page_to_ready(site, url, meta={}):
    with Connection.cursor() as cur:
        try:
            cur.execute(
                """
                INSERT INTO osint.pages (site, url, meta, status) VALUES (%s, %s, %s, %s) RETURNING id
            """,
                [
                    site,
                    url,
                    Jsonb(meta),
                    PageStatus.ready,
                ],
            )
            Connection.commit()
            response = cur.fetchone()
            if response:
                id = response[0]
                return id
        except Exception as err:
            Connection.rollback()
            return err


def update_page_to_crawling(page_id, meta={}):
    with Connection.cursor() as cur:
        try:
            cur.execute(
                """
                UPDATE osint.pages
                SET meta = %s,
                    updated_at = %s,
                    status = %s
                WHERE id = %s
            """,
                [
                    Jsonb(meta),
                    datetime.datetime.now(datetime.UTC),
                    PageStatus.crawling,
                    page_id,
                ],
            )
            Connection.commit()
        except Exception as err:
            Connection.rollback()
            return err


def update_page_to_recrawl(page_id, meta={}):
    with Connection.cursor() as cur:
        try:
            cur.execute(
                """
                UPDATE osint.pages
                SET meta = %s,
                    updated_at = %s,
                    status = %s
                WHERE id = %s
            """,
                [
                    Jsonb(meta),
                    datetime.datetime.now(datetime.UTC),
                    PageStatus.ready,
                    page_id,
                ],
            )
            Connection.commit()
        except Exception as err:
            Connection.rollback()
            return err


def update_crawled_page(page_id, meta={}):
    with Connection.cursor() as cur:
        try:
            cur.execute(
                """
                UPDATE osint.pages
                SET meta = %s,
                    status = %s,
                    updated_at = %s
                WHERE id = %s
            """,
                [
                    Jsonb(meta),
                    PageStatus.finished,
                    datetime.datetime.now(datetime.UTC),
                    page_id,
                ],
            )
            Connection.commit()
        except Exception as err:
            Connection.rollback()
            return err


def update_failed_crawl_page(page_id, meta={}):
    with Connection.cursor() as cur:
        try:
            cur.execute(
                """
                UPDATE osint.pages
                SET meta = %s,
                    status = %s,
                    updated_at = %s
                WHERE id = %s
            """,
                [
                    Jsonb(meta),
                    PageStatus.failed,
                    datetime.datetime.now(datetime.UTC),
                    page_id,
                ],
            )
            Connection.commit()
        except Exception as err:
            Connection.rollback()
            return err


def get_page_by_id(page_id):
    with Connection.cursor(row_factory=class_row(Page)) as cur:
        result = cur.execute(
            """
            SELECT * FROM osint.pages WHERE id = %s
        """,
            [
                page_id,
            ],
        ).fetchone()
        return result


def get_page_by_url(site, url):
    with Connection.cursor(row_factory=class_row(Page)) as cur:
        result = cur.execute(
            """
            SELECT * FROM osint.pages WHERE site = %s AND url = %s
        """,
            [
                site,
                url,
            ],
        ).fetchone()
        return result


def page_exists(site, url):
    return get_page_by_url(site, url) is not None


def get_ready_pages(site):
    with Connection.cursor(row_factory=class_row(Page)) as cur:
        result = cur.execute(
            """
            SELECT * FROM osint.pages WHERE site = %s AND status = %s
        """,
            [site, PageStatus.ready],
        ).fetchall()
        return result


def get_finished_pages():
    with Connection.cursor(row_factory=class_row(Page)) as cur:
        result = cur.execute(
            """
            SELECT * FROM osint.pages WHERE status = %s
        """,
            [PageStatus.finished],
        ).fetchall()
        return result


def add_ioc(type, key):
    with Connection.cursor() as cur:
        try:
            cur.execute(
                """
                INSERT INTO osint.iocs (type, key) VALUES (%s, %s) RETURNING id
            """,
                [
                    type,
                    key,
                ],
            )
            Connection.commit()
            response = cur.fetchone()
            if response:
                id = response[0]
                return id
        except Exception as err:
            Connection.rollback()
            return err


def get_ioc_by_id(ioc_id):
    with Connection.cursor(row_factory=class_row(Ioc)) as cur:
        result = cur.execute(
            """
            SELECT * FROM osint.iocs WHERE id = %s
        """,
            [
                ioc_id,
            ],
        ).fetchone()
        return result


def get_ioc_by_key(key):
    with Connection.cursor(row_factory=class_row(Ioc)) as cur:
        result = cur.execute(
            """
            SELECT * FROM osint.iocs WHERE key = %s
        """,
            [
                key,
            ],
        ).fetchone()
        return result


def add_relation(iocs_id, pages_id):
    with Connection.cursor() as cur:
        try:
            cur.execute(
                """
                INSERT INTO osint.relations
                (iocs_id, pages_id) VALUES
                (%s, %s) RETURNING id
            """,
                [
                    iocs_id,
                    pages_id,
                ],
            )
            Connection.commit()
            response = cur.fetchone()
            if response:
                id = response[0]
                return id
        except Exception as err:
            Connection.rollback()
            return err


def get_relation_by_ids(iocs_id, pages_id):
    with Connection.cursor(row_factory=class_row(Relation)) as cur:
        result = cur.execute(
            """
            SELECT * FROM osint.relations WHERE iocs_id = %s and pages_id = %s
        """,
            [
                iocs_id,
                pages_id,
            ],
        ).fetchone()
        return result


if __name__ == "__main__":
    # add_page_to_crawl("isa", "testurl", {"ab": 123})
    # update_crawled_page(2, "content", {"abc": 456})
    print("rrrrrrrrrr")
    pages = get_finished_pages()
    print(pages)
    print(pages[0])
    pass

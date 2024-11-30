#!/usr/bin/env python3
import sys
import json
import logging
import argparse
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, asdict

PARENT_DIRECTORY = Path(__file__).parent
CRYPTO_PROJECTS_PATH = PARENT_DIRECTORY / "crypto-projects.json"


@dataclass
class Descriptions:
    short: str
    long: str


@dataclass
class Requirements:
    task: str
    difficulty: str


@dataclass
class Rewards:
    amount: int
    distribution_date: datetime


@dataclass
class Links:
    official_website: str
    twitter: str
    reddit: str
    github: str


@dataclass
class CryptoProject:
    project: str
    descriptions: Descriptions
    requirements: Requirements
    rewards: Rewards
    status: str
    deadline: datetime
    last_updated: datetime
    groups: list
    links: Links


def search_by_task(projects: list[CryptoProject], task: str) -> list[CryptoProject]:
    tasked_projects = [project for project in projects if project.requirements["task"] == task]
    return tasked_projects


def filter_by_status(projects: list[CryptoProject], status: str) -> list[CryptoProject]:
    status_projects = [project for project in projects if project.status == status]
    return status_projects


def group(projects: list[CryptoProject], group_name: str) -> None:
    for project in projects:
        if not group_name in project.groups:
            project.groups.append(group_name)


def setup_logger() -> logging.Logger:
    logger = logging.getLogger('crypto-project-processor')
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler())
    return logger


def validate_all_grouped_projects_exist(projects_to_group: list[str], project_names: list[str]) -> bool:
    # We will use set difference to find if there are any elements in projects_to_group that do not exist in
    # project_names, thus validating user doesn't try to create a group with a nonexistent project.
    projects_to_group, project_names = set(projects_to_group), set(project_names)
    nonexistent_projects = projects_to_group - project_names
    return len(nonexistent_projects) == 0


def serialize_datetime(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    return obj


def dispatch_and_run(args: argparse.Namespace, logger: logging.Logger) -> None:
    with open(CRYPTO_PROJECTS_PATH, "r+", encoding="utf-8") as file:
        projects = [CryptoProject(**project) for project in json.load(file)]
    if args.searched_task:
        tasked_projects = search_by_task(projects, args.searched_task)
        tasked_project_names = [project.project for project in tasked_projects]
        if not tasked_project_names:
            logger.info(f"No projects found for the task \"{args.searched_task}\"")
        else:
            logger.info(f"{tasked_project_names} are labelled with the task \"{args.searched_task}\"")
    if args.searched_status:
        status_projects = filter_by_status(projects, args.searched_status)
        status_project_names = [project.project for project in status_projects]
        if not status_project_names:
            logger.info(f"No projects are currently {args.searched_status}")
        else:
            logger.info(f"{status_project_names} currently {args.searched_status}")
    if args.grouped_projects and args.as_name:
        projects_to_group = args.grouped_projects.split(',')
        if len(projects_to_group) == 1:
            raise RuntimeError(f"--group requires multiple projects to be listed with a comma but no comma was found.")
        project_names = [project.project for project in projects]
        if not validate_all_grouped_projects_exist(projects_to_group, project_names):
            raise ValueError("Group contains nonexistent projects.")
        group(projects, args.as_name)
        serialized_projects = [asdict(project) for project in projects]
        with open(CRYPTO_PROJECTS_PATH, "w", encoding="utf-8") as file:
            file.truncate(0)  # Clears the file before we dump a new JSON into it.
            json.dump(serialized_projects, file, default=serialize_datetime, indent=2)


def main():
    parser = argparse.ArgumentParser("crypto-project-processor")
    commands = parser.add_argument_group('required arguments')
    commands.add_argument("-v", "--version", action="version", version="%(prog)s v1.0")
    commands.add_argument("--search-by-task", action="store", dest="searched_task",
                          help="Find crypto project by tasks.")
    commands.add_argument("--search-by-status", action="store", dest="searched_status",
                          help="Find crypto project by status.")
    commands.add_argument("--group", action="store", dest="grouped_projects",
                          help="Create a new group of crypto projects.")
    commands.add_argument("--as", action="store", dest="as_name",
                          help="The name of new crypto group.")

    args = parser.parse_args()
    logger = setup_logger()

    if not any([args.searched_task, args.searched_status, args.grouped_projects]):
        parser.error("At least one command (--search-by-task, --search-by-status, or --group) is required")

    if args.grouped_projects and not args.as_name:
        parser.error("When using --group, you must specify a name with --as")

    try:
        dispatch_and_run(args, logger)
    except RuntimeError as e:
        logger.error(e)
        sys.exit(1)
    except ValueError as e:
        logger.error(e)
        sys.exit(1)


if __name__ == "__main__":
    main()

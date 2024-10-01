#!/usr/bin/env python3

import fitz
import csv
import re
import logging
import argparse
import sys

def parse_cis_benchmark(pdf_file, out_file):
    # Initialize variables
    (
        rule_count,
        level_count,
        description_count,
        acnt,
        rat_count,
        rem_count,
        defval_count,
        cis_count,
    ) = (0,) * 8
    firstPage = None
    seenList = []

    # Setup logging
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        logging_streamhandler = logging.StreamHandler(stream=None)
        logging_streamhandler.setFormatter(
            logging.Formatter(fmt="%(asctime)s %(levelname)-8s %(message)s")
        )
        logger.addHandler(logging_streamhandler)

    # Open PDF File
    doc = fitz.open(pdf_file)

    # Get CIS Type from the name of the document in the cover page
    coverPageText = doc.load_page(0).get_text("text")
    logger.debug(coverPageText)
    try:
        pattern = "(?<=CIS).*(?=Benchmark)"
        rerule = re.search(pattern, coverPageText, re.DOTALL)
        if rerule is not None:
            CISName = rerule.group(0).strip().replace('\n','')
            logger.info("*** Document found name: {} ***".format(CISName))
            if "Apache Tomcat 8" in CISName:
                pattern = "(\d+(?:\.\d.\d*)+)(.*?)(\(Automated\)|\(Manual\)|\(Scored\)|\(Not Scored\))"
            elif "Apache Tomcat 10" in CISName:
                pattern = "(\d+(?:\.\d.\d*)+)(.*?)(\(Automated\)|\(Manual\))"
            elif "Red Hat Enterprise Linux 7" in CISName:
                pattern = "(\d+(?:\.\d.\d*)+)(.*?)(\(Automated\)|\(Manual\))"
            elif "Debian Linux 11" in CISName:
                pattern = "(\d+(?:\.\d.\d*)+)(.*?)(\(Automated\)|\(Manual\))"
            elif "CentOS Linux 7" in CISName:
                pattern = "(\d+(?:\.\d.\d*)+)(.*?)(\(Automated\)|\(Manual\))"
            elif "Microsoft Windows Server 2012" in CISName:
                pattern = "(\d+(?:\.\d+)+)\s\(((L[12])|(NG))\)(.*?)(\(Automated\)|\(Manual\))"
            elif "Microsoft Windows Server 2019" in CISName:
                pattern = "(\d+(?:\.\d+)+)\s\(((L[12])|(NG))\)(.*?)(\(Automated\)|\(Manual\))"
            elif "Microsoft Windows Server 2022" in CISName:
                pattern = "(\d+(?:\.\d+)+)\s\(((L[12])|(NG))\)(.*?)(\(Automated\)|\(Manual\))"
            elif "Microsoft Windows 10 Enterprise" in CISName:
                pattern = "(\d+(?:\.\d+)+)\s\(((L[12])|(NG)|(BL))\)(.*?)(\(Automated\)|\(Manual\))"
            elif "Ubuntu Linux 18.04 LTS" in CISName:
                pattern = "(\d+(?:\.\d.\d*)+)(.*?)(\(Automated\)|\(Manual\))"
            else:
                raise ValueError("Could not find a matching regex for {}".format(CISName))
    except IndexError:
        logger.error("*** Could not find CIS Name, exiting. ***")
        return

    # Skip to actual rules
    for currentPage in range(len(doc)):
        findPage = doc.load_page(currentPage)
        if findPage.search_for("Recommendations 1 "):
            firstPage = currentPage

    # If no "Recommendations" and "Initial Setup" it is not a full CIS Benchmark .pdf file
    if firstPage is None:
        logger.error("*** Not a CIS PDF Benchmark, exiting. ***")
        return

    logger.info("*** Total Number of Pages: %i ***", doc.page_count)

    # Open output .csv file for writing
    with open(out_file, mode="w") as cis_outfile:
        rule_writer = csv.writer(
            cis_outfile, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL
        )
        rule_writer.writerow(
            [
                "Rule",
                "Profile Applicability",
                "Description",
                "Rationale",
                "Audit",
                "Remediation",
                "Default Value",
                "CIS Controls",
            ]
        )

        # Loop through all PDF pages
        for page in range(firstPage, len(doc)):
            if page < len(doc):
                data = doc.load_page(page).get_text("text")
                logger.info("*** Parsing Page Number: %i ***", page)

                # Initialize variables for each iteration
                rule = ""
                level = ""
                description = ""
                rat = ""
                audit = ""
                rem = ""
                defval = ""
                cis = ""

                # Get rule by matching regex pattern for x.x.* (Automated) or (Manual)
                try:
                    rerule = re.search(pattern, data, re.DOTALL)
                    if rerule is not None:
                        rule = rerule.group()
                        rule_count += 1
                    else:
                        logger.info("*** No rule found on this page, skipping... ***")
                        continue
                except (IndexError, AttributeError):
                    logger.info("*** Page does not contain a Rule Name, skipping... ***")
                    continue

                # Get Profile Applicability
                try:
                    l_post = data.split("Profile Applicability:", 1)[1]
                    level = l_post.partition("Description:")[0].strip()
                    level = re.sub("[^a-zA-Z0-9\\n-]+", " ", level)
                    level_count += 1
                except IndexError:
                    logger.info("*** Page does not contain Profile Levels ***")

                # Get Description
                try:
                    d_post = data.split("Description:", 1)[1]
                    description = d_post.partition("Rationale")[0].strip()
                    description_count += 1
                except IndexError:
                    logger.info("*** Page does not contain Description ***")

                # Get Rationale
                try:
                    rat_post = data.split("Rationale:", 1)[1]
                    rat = rat_post.partition("Audit:")[0].strip()
                    rat_count += 1
                except IndexError:
                    logger.info("*** Page does not contain Rationale ***")

                # Get Audit
                try:
                    a_post = data.split("\nAudit:", 1)[1]
                    audit = a_post.partition("Remediation")[0].strip()
                    acnt += 1
                except IndexError:
                    logger.info("*** Page does not contain Audit ***")

                # Get Remediation
                try:
                    rem_post = data.split("Remediation:", 1)[1]
                    rem = rem_post.partition("Default Value:")[0].strip()
                    rem_count += 1
                except IndexError:
                    logger.info("*** Page does not contain Remediation ***")

                # Get Default Value
                try:
                    defval_post = data.split("Default Value:", 1)[1]
                    defval = defval_post.partition("CIS Controls:")[0].strip()
                    defval_count += 1
                except IndexError:
                    logger.info("*** Page does not contain Default Value ***")

                # Get CIS Controls
                try:
                    cis_post = data.split("CIS Controls:", 1)[1]
                    cis = cis_post.partition("P a g e")[0].strip()
                    cis = re.sub("[^a-zA-Z0-9\\n.-]+", " ", cis)
                    cis_count += 1
                    if defval_count == (cis_count-1):
                        defval = ""
                        defval_count += 1
                except IndexError:
                    logger.info("*** Page does not contain CIS Controls ***")

                # Write to csv if a parsed rule is fully assembled
                row = [rule, level, description, rat, audit, rem, defval, cis]
                rule_writer.writerow(row)
                logger.info("*** Writing rule to csv: %s ***", rule)

            else:
                logger.info("*** All pages parsed, exiting. ***")
                break

    logger.info("*** Parsing complete, CSV file created: %s ***", out_file)

def main():
    parser = argparse.ArgumentParser(
        description="Parses CIS Benchmark PDF content into CSV Format"
    )
    required = parser.add_argument_group("required arguments")
    required.add_argument(
        "--pdf_file", type=str, required=True, help="PDF File to parse"
    )
    required.add_argument(
        "--out_file", type=str, required=True, help="Output file in .csv format"
    )
    required.add_argument(
        '-l', '--log-level', type=str, required=False, help="Set log level (DEBUG, INFO, etc). Default to INFO",
        default="INFO"
    )
    args = parser.parse_args()

    logging.basicConfig(level=args.log_level)
    
    parse_cis_benchmark(args.pdf_file, args.out_file)

if __name__ == "__main__":
    main()
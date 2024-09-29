
from weasyprint import HTML
import random
def generate_pdf(tree,title):


    # Create HTML content
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Case Summary</title>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');

            @page {{
                margin: 14px; /* Set consistent margin for all pages */
                size: A4;
            }}
            body {{
                font-family: 'Roboto', sans-serif; /* Use Roboto font */
                margin: 0; /* Set body margin to 0 */
                padding: 10px; /* Add padding as needed */
                background-color: #f0f8ff;
                color: #333;
            }}
            h1 {{
                text-align: center;
                color: #2c3e50;
                font-size: 2.5em;
                margin-bottom: 20px;
                text-transform: uppercase;
            }}
            h2 {{
                color: #2980b9;
                border-bottom: 2px solid #2980b9;
                padding-bottom: 10px;
                margin: 30px 0 15px 0; /* Increased vertical space */
                font-size: 2em; /* Slightly larger */
            }}
            h3 {{
                color: #c0392b;
                margin: 20px 0;
                font-size: 1.6em;
            }}
            p {{
                font-size: 16px;
                line-height: 1.6;
                margin: 10px 0;
            }}
            ul {{
                list-style-type: none;
                padding: 0;
                margin: 15px 0;
            }}
            li {{
                margin-bottom: 15px;
                padding: 15px;
                background-color: #ffffff;
                border: 1px solid #ddd;
                border-radius: 5px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
                transition: background-color 0.3s;
            }}
            li:hover {{
                background-color: #e0f7fa; /* Light hover effect */
            }}
            .important {{
                color: #c0392b;
                font-weight: bold;
            }}
            .info, .date {{
                color: #2980b9;
            }}
            footer {{
                text-align: center;
                margin-top: 40px; /* Adjusted margin for footer */
                font-size: 12px;
                color: #777;
            }}
        </style>
    </head>
    <body>
        <h1>Case Summary</h1>
        <h2>Title: {title}</h2>
        <h2>Case Overview</h2>
        <p>{tree.get("caseoverview", {}).get("detail_text", "No Case Overview Found")}</p>

        <h2>Places</h2>
        </ul>

    </body>
    </html>
    """

    for place in tree.get("caseoverview", {}).get("places", []):
        html_content += f"<li><span class='important'>Name:</span> {place.get('name', 'No Name')}<br/><span class='date'>Date:</span> {place.get('date', 'Date Not Provided')}</li>"
    html_content += "</ul>"


    # Add People
    html_content += "<h2>People</h2><ul>"
    for person in tree.get("caseoverview", {}).get("people", []):
        html_content += f"<li><span class='important'>Name:</span> {person.get('name', 'No Name')}<br/><span class='important'>Role:</span> {person.get('role', 'No Role')}<br/><span class='info'>Info:</span> {person.get('info', 'No Info')}</li>"
    html_content += "</ul>"


    # Add Organizations
    html_content += "<h2>Organizations</h2><ul>"
    for organization in tree.get("caseoverview", {}).get("organizations", []):
        html_content += f"<li><span class='important'>Name:</span> {organization.get('name', 'No Name')}<br/><span class='important'>Role:</span> {organization.get('role', 'No Role')}<br/><span class='info'>Info:</span> {organization.get('info', 'No Info')}</li>"
    html_content += "</ul>"


    # Add Timeline
    html_content += "<h2>Timeline</h2><ul>"
    for event in tree.get("caseoverview", {}).get("timeline", []):
        html_content += f"<li><span class='date'>Date:</span> {event.get('date', 'Date Not Provided')}<br/><span class='important'>Event:</span> {event.get('event', 'No Description')}</li>"
    html_content += "</ul>"


    # Add Actions Taken
    html_content += "<h2>Actions Taken</h2><ul>"
    for action in tree.get("caseoverview", {}).get("actions_taken", []):
        html_content += f"<li><span class='important'>Action:</span> {action.get('action', 'No Action')}<br/><span class='important'>By:</span> {action.get('by', 'No Responsible Party')}</li>"
    html_content += "</ul>"


    # Add Claims
    html_content += "<h2>Claims</h2><ul>"
    for claim in tree.get("caseoverview", {}).get("claims", []):
        html_content += f"<li><span class='important'>Claim:</span> {claim.get('claim', 'No Claim')}<br/><span class='important'>By:</span> {claim.get('by', 'No Party')}</li>"
    html_content += "</ul>"


    # Add Legal Framework
    html_content += "<h2>Legal Framework</h2>"
    html_content += "<h3>Strengths</h3><ul>"
    for strength in tree.get("legalframework", {}).get("strengths", []):
        html_content += f"<li>{strength}</li>"
    html_content += "</ul>"


    html_content += "<h3>Weaknesses</h3><ul>"
    for weakness in tree.get("legalframework", {}).get("weaknesses", []):
        html_content += f"<li>{weakness}</li>"
    html_content += "</ul>"


    html_content += "<h3>Rules</h3><ul>"
    for rule in tree.get("legalframework", {}).get("rules", []):
        html_content += f"<li><span class='important'>Rule:</span> {rule.get('rule', 'No Rule')}<br/><span>Reason:</span> {rule.get('reason', 'No Reason')}</li>"
    html_content += "</ul>"


    html_content += "<h3>Past Judgments</h3><ul>"
    for judgment in tree.get("legalframework", {}).get("pastjudgments", []):
        file_link = judgment.get('filelink', 'No File')
        if file_link != 'No File':
            file_link = f"<a href='{file_link}'>{file_link}</a>"
        html_content += f"<li><span class='important'>Citation:</span> {judgment.get('citation', 'No Citation')}<br/><span>Reason:</span> {judgment.get('reason', 'No Reason')}<br/><span class='important'>File:</span> {file_link}</li>"
    html_content += "</ul>"


    # Add Evidence and Support
    html_content += "<h2>Evidence and Support</h2><ul>"
    for evidence in tree.get("evidence_and_support", {}).get("detailed_evidence", []):
        html_content += f"<li>{evidence}</li>"
    html_content += "</ul>"


    # Add Case Strategy
    html_content += "<h2>Case Strategy</h2><ul>"
    for strategy in tree.get("case_strategy", {}).get("legal_strategies", []):
        html_content += f"<li>{strategy}</li>"
    html_content += "</ul>"


    html_content += "<h3>Opposition Weaknesses</h3><ul>"
    for weakness in tree.get("case_strategy", {}).get("opposition_weaknesses", []):
        html_content += f"<li>{weakness}</li>"
    html_content += "</ul>"


    html_content += "<h3>Defense Arguments</h3><ul>"
    for defense in tree.get("case_strategy", {}).get("defenses_for_opposite", []):
        html_content += f"<li>{defense}</li>"
    html_content += "</ul>"


    html_content += "<h3>Cross-examination Questions</h3><ul>"
    for question in tree.get("case_strategy", {}).get("cross_examination_questions", []):
        html_content += f"<li>{question}</li>"
    html_content += "</ul>"
   
        # Add Risk and Outcome Analysis
    html_content += "<h2>Risk and Outcome Analysis</h2>"


    # Potential Outcomes
    html_content += "<h3>Potential Outcomes</h3><ul>"
    for outcome in tree.get("risk_and_outcome_analysis", {}).get("potential_outcomes", []):
        html_content += f"<li>{outcome}</li>"
    html_content += "</ul>"


    # Risk Factors
    html_content += "<h3>Risk Factors</h3><ul>"
    for risk in tree.get("risk_and_outcome_analysis", {}).get("risk_analysis", []):
        html_content += f"<li>{risk}</li>"
    html_content += "</ul>"


    # Add Financial Impact
    html_content += "<h3>Financial Impact </h3><ul>"
    for finance in tree.get("risk_and_outcome_analysis", {}).get("financial_impact", []):
        html_content += f"<li>{finance}</li>"
    html_content += "</ul>"


    # Add Appeal Potential
    html_content += "<h3>Appeal Potential</h3><ul>"
    for appeal in tree.get("risk_and_outcome_analysis", {}).get("appeal_potential", []):
        html_content += f"<li>{appeal}</li>"
   


    # Add Settlement and Negotiation
    html_content += "<h2>Settlement and Negotiation</h2>"


      # settlement_options
    html_content += "<h3>Settlement Options</h3><ul>"
    for Settlement in tree.get("settlement_and_negotiation", {}).get("settlement_options", []):
        html_content += f"<li>{Settlement}</li>"
    html_content += "</ul>"
   
     # negotiation_tactics
    html_content += "<h3>Negotiation Tactics</h3><ul>"
    for Negotiation in tree.get("settlement_and_negotiation", {}).get("negotiation_tactics", []):
        html_content += f"<li>{Negotiation}</li>"
    html_content += "</ul>"




    # Add Courtroom and Trial Management
    html_content += "<h2>Courtroom and Trial Management</h2>"


   
      # settlement_options
    html_content += "<h3>Courtroom Procedures</h3><ul>"
    for courtroom in tree.get("courtroom_and_trial_management", {}).get("courtroom_procedures", []):
        html_content += f"<li>{courtroom}</li>"
    html_content += "</ul>"




    # document_checklist
    html_content += "<h3>Document Checklist</h3><ul>"
    for checklist in tree.get("courtroom_and_trial_management", {}).get("document_checklist", []):
        html_content += f"<li>{checklist}</li>"


    # public_relations_and_client_communication
    html_content += "<h2>Public Relations and Client Communication</h2>"


    # public_relations_impact
    html_content += "<h3>Public Relations Impact</h3><ul>"
    for impact in tree.get("public_relations_and_client_communication", {}).get("public_relations_impact", []):
        html_content += f"<li>{impact}</li>"


    # client_communication
    html_content += "<h3>Client Communication</h3><ul>"
    for communication in tree.get("public_relations_and_client_communication", {}).get("client_communication", []):
        html_content += f"<li>{communication}</li>"




    html_content += "</body></html>"


    # Convert HTML to PDF
    pdf_file_path = f"case_summary{random.randint(11,99)}.pdf"
    HTML(string=html_content).write_pdf(pdf_file_path)


    print(f"PDF generated successfully: {pdf_file_path}")

    return pdf_file_path

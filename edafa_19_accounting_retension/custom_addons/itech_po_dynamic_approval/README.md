# Dynamic Purchase Order Approval

## Overview

**Dynamic Purchase Order Approval** is a comprehensive Odoo 19 module that provides a flexible, multi-level approval system for Purchase Orders. This module enables organizations to implement customizable approval workflows where multiple team members must approve purchase orders before they can be confirmed.

## Key Features

✅ **Multi-Level Approval System** - Require approvals from multiple team members  
✅ **Flexible Team Configuration** - Create custom approval teams with team leads and members  
✅ **Automatic Approval Routes** - Approval routes are automatically created when a PO is assigned to a team  
✅ **Team Lead Override** - Team leads can bypass the approval process and confirm POs directly  
✅ **Real-Time Approval Tracking** - View approval status for each team member  
✅ **User-Friendly Interface** - Simple approve/reject buttons with visual feedback  
✅ **Role-Based Approval** - Assign roles to team members for better organization  

## Module Information

- **Name:** Dynamic Purchase Order Approval/Purchase Approval
- **Version:** 19.0.1.0
- **Author:** iTech Co.
- **License:** LGPL-3
- **Category:** Purchase
- **Dependencies:** base, purchase
- **Odoo Version:** 19.0

## Installation

1. Copy the module to your Odoo addons path
2. Update the Apps list in Odoo
3. Search for "Dynamic Purchase Order Approval"
4. Click Install

## Quick Start

1. **Create an Approval Team:**
   - Go to: Purchase → Configuration → PO Approval Teams
   - Create a new team with a short code, name, team lead, and members

2. **Assign Team to Purchase Order:**
   - When creating a PO, select the approval team
   - Approval routes are automatically created for all team members

3. **Approve Purchase Orders:**
   - Team members see "Approve" and "REJECT" buttons on POs
   - Click to approve or reject
   - PO cannot be confirmed until all members approve (unless team lead confirms)

## Architecture

### Models

- **purchase.order.teams** - Approval teams configuration
- **purchase.team.member** - Team members with roles and amount limits
- **purchase.approve.route** - Approval tracking for each PO
- **purchase.order** - Extended with approval functionality

### Workflow

1. PO created → Approval team assigned → Approval routes created
2. Team members approve/reject → Status tracked
3. All approvals required → PO can be confirmed
4. Team lead can bypass → Direct confirmation possible

## Use Cases

### Use Case 1: Department-Based Approval
**Scenario:** Different departments require different approval processes.

**Solution:** Create separate approval teams for each department (e.g., IT Team, HR Team, Finance Team) with department-specific members and leads.

### Use Case 2: Amount-Based Approval
**Scenario:** Higher value purchases require more approvals.

**Solution:** Create teams with members having min/max amount limits. Assign appropriate teams based on PO value.

### Use Case 3: Multi-Stage Approval
**Scenario:** Purchases need approval from multiple levels (Manager → Director → CFO).

**Solution:** Create a team with all required approvers. Each must approve before confirmation.

### Use Case 4: Emergency Purchases
**Scenario:** Urgent purchases need team lead override capability.

**Solution:** Team leads can directly confirm POs without waiting for all member approvals.

### Use Case 5: Role-Based Approval
**Scenario:** Different approvers have different roles (Technical Reviewer, Budget Approver, Legal Reviewer).

**Solution:** Assign roles to team members. Track which role approved each PO.

## Configuration

### Creating an Approval Team

1. Navigate to: **Purchase → Configuration → PO Approval Teams**
2. Click **Create**
3. Fill in:
   - **Short Code:** Unique identifier (e.g., "IT_PO", "HR_PO")
   - **Name:** Descriptive name (e.g., "IT Department Approval Team")
   - **Team Lead:** User who can bypass approvals
4. Add team members in the **Members** tab:
   - **Team Members:** Select users
   - **Role:** Optional role description
   - **Minimum/Maximum Amount:** Optional amount limits

### Default Team

A default team ("DefaultPO") is created automatically. You can modify it or create new teams as needed.

## Security

- Only team members can approve/reject POs assigned to their team
- Team leads have special privileges to confirm POs directly
- Purchase managers can configure teams and view all approvals

## Troubleshooting

### PO Cannot Be Confirmed
- **Issue:** Error message about pending approvals
- **Solution:** Ensure all team members have approved, or have the team lead confirm the PO

### Approve Button Not Visible
- **Issue:** User doesn't see approve/reject buttons
- **Solution:** Verify the user is a member of the assigned approval team

### Approval Routes Not Created
- **Issue:** No approval routes appear after assigning team
- **Solution:** Check that the team has members assigned

## Support

For issues, questions, or feature requests, please contact iTech Co.

## License

This module is licensed under LGPL-3.

---

**Version:** 19.0.1.0  
**Last Updated:** December 2025


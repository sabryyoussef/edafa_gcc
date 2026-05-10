# User Guide: Dynamic Purchase Order Approval

## Table of Contents

1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
3. [Setting Up Approval Teams](#setting-up-approval-teams)
4. [Using Approval Workflows](#using-approval-workflows)
5. [Detailed Use Cases](#detailed-use-cases)
6. [Best Practices](#best-practices)
7. [FAQ](#faq)

---

## Introduction

The **Dynamic Purchase Order Approval** module enhances Odoo's purchase management by adding a flexible, multi-level approval system. This guide will help you understand and effectively use all features of the module.

### What This Module Does

- Enforces multi-member approval before PO confirmation
- Provides team-based approval workflows
- Allows team leads to override approval requirements
- Tracks approval status in real-time
- Supports role-based approval assignments

---

## Getting Started

### Prerequisites

- Odoo 19.0 installed
- Purchase module installed
- Appropriate user permissions (Purchase User/Manager)

### Initial Setup

1. **Install the Module**
   - Go to Apps menu
   - Remove "Apps" filter
   - Search for "Dynamic Purchase Order Approval"
   - Click Install

2. **Verify Installation**
   - Navigate to: Purchase → Configuration
   - You should see "PO Approval Teams" menu item

3. **Check Default Team**
   - Go to: Purchase → Configuration → PO Approval Teams
   - A default team "PO Approval Team" should exist
   - Review and modify as needed

---

## Setting Up Approval Teams

### Creating a New Approval Team

**Step 1: Access Team Configuration**
- Navigate to: **Purchase → Configuration → PO Approval Teams**
- Click **Create**

**Step 2: Basic Information**
```
Short Code: IT_PO_APPROVAL
Name: IT Department Purchase Approval Team
Team Lead: [Select IT Manager]
```

**Step 3: Add Team Members**
- Click on the **Members** tab
- Click **Add a line**
- For each member, fill in:
  - **Team Members:** Select user
  - **Role:** (Optional) e.g., "Technical Reviewer", "Budget Approver"
  - **Minimum Amount:** (Optional) Minimum PO amount for this approver
  - **Maximum Amount:** (Optional) Maximum PO amount for this approver

**Example Team Setup:**
```
Team: IT Department Approval Team
Team Lead: John Smith (IT Manager)

Members:
1. Alice Johnson - Role: Technical Reviewer
2. Bob Williams - Role: Budget Approver
3. Carol Davis - Role: Security Reviewer
```

### Modifying Existing Teams

1. Open the team from the list
2. Update fields as needed
3. Add/remove members in the Members tab
4. Save changes

**Note:** Changes to team membership will affect new POs. Existing POs keep their original approval routes.

---

## Using Approval Workflows

### Scenario 1: Creating a Purchase Order with Approval

**Step 1: Create Purchase Order**
1. Go to: **Purchase → Purchase Orders → Create**
2. Fill in vendor, products, quantities, etc.
3. In the **Approval Team** field, select your approval team
4. The **Purchase Team Lead** field will auto-populate
5. Save the PO

**Step 2: Automatic Approval Route Creation**
- Once saved, approval routes are automatically created
- Go to the **Approve Route** tab to see all approvers
- Each team member will have a "Pending" status

**Step 3: Approval Process**
- Team members will see "Approve" and "REJECT" buttons
- Each member must approve before PO can be confirmed
- Status updates in real-time

### Scenario 2: Approving a Purchase Order

**As a Team Member:**

1. **Access the PO**
   - Go to: **Purchase → Purchase Orders**
   - Open the PO assigned to your team

2. **Review the PO**
   - Check all details (vendor, products, amounts, terms)
   - Review the **Approve Route** tab to see other approvers' status

3. **Approve or Reject**
   - Click **Approve** button (green, highlighted)
     - Confirmation dialog appears
     - Click OK to approve
     - Success message with visual feedback
   - OR
   - Click **REJECT** button (red)
     - Confirmation dialog appears
     - Click OK to reject
     - PO approval is cancelled

4. **Check Status**
   - Your approval status changes to "Approved" or "Cancelled"
   - Other team members can see your decision

**Important Notes:**
- You can only approve/reject once per PO
- If you reject, you can change to approve later (and vice versa)
- Your approval is visible to all team members

### Scenario 3: Team Lead Override

**As a Team Lead:**

1. **Access the PO**
   - Open any PO assigned to your team

2. **Review Approval Status**
   - Check the **Approve Route** tab
   - See which members have approved/rejected

3. **Direct Confirmation (If Needed)**
   - If urgent, you can confirm the PO directly
   - Click **Confirm Order** button
   - PO will be confirmed even if some members haven't approved
   - This bypasses the approval requirement

**When to Use Override:**
- Emergency purchases
- Time-sensitive orders
- When you trust the purchase but need speed

**Best Practice:** Use override sparingly and document the reason.

### Scenario 4: Confirming a Purchase Order

**Standard Confirmation (All Approvals Required):**

1. **Check Approval Status**
   - Open the PO
   - Go to **Approve Route** tab
   - Verify all members show "Approved" status

2. **Confirm Order**
   - Click **Confirm Order** button
   - PO will be confirmed successfully

**If Approvals Missing:**
- Error message will appear
- Lists which approvers haven't approved yet
- Must wait for all approvals OR have team lead confirm

---

## Detailed Use Cases

### Use Case 1: IT Department Hardware Purchase

**Business Need:** IT department needs to purchase laptops. Multiple stakeholders must approve.

**Setup:**
```
Team: IT Hardware Approval
Team Lead: IT Director
Members:
  - IT Manager (Technical Reviewer)
  - Finance Manager (Budget Approver)
  - Procurement Manager (Vendor Reviewer)
```

**Workflow:**
1. IT staff creates PO for 20 laptops
2. Assigns "IT Hardware Approval" team
3. Approval routes created for 3 members
4. IT Manager approves (technical specs OK)
5. Finance Manager approves (budget available)
6. Procurement Manager approves (vendor terms OK)
7. PO confirmed automatically

**Result:** All stakeholders reviewed and approved before purchase.

---

### Use Case 2: High-Value Purchase with Escalation

**Business Need:** Purchase over $50,000 requires CFO approval.

**Setup:**
```
Team: High-Value Approval
Team Lead: CFO
Members:
  - Department Manager (min: $0, max: $10,000)
  - Finance Director (min: $10,000, max: $50,000)
  - CFO (min: $50,000, max: unlimited)
```

**Workflow:**
1. PO created for $75,000 equipment
2. System assigns "High-Value Approval" team
3. All three members see the PO
4. Department Manager approves
5. Finance Director approves
6. CFO approves (required for this amount)
7. PO confirmed

**Result:** Appropriate approval levels based on purchase value.

---

### Use Case 3: Emergency Purchase with Override

**Business Need:** Urgent server replacement needed immediately.

**Setup:**
```
Team: IT Emergency Approval
Team Lead: IT Director
Members:
  - IT Manager
  - Finance Manager
```

**Workflow:**
1. PO created for emergency server
2. Assigned to "IT Emergency Approval" team
3. IT Manager approves quickly
4. Finance Manager is unavailable
5. IT Director (team lead) uses override
6. PO confirmed immediately without waiting

**Result:** Business continuity maintained while maintaining some approval oversight.

---

### Use Case 4: Multi-Department Collaboration

**Business Need:** Marketing campaign requires purchases from multiple departments.

**Setup:**
```
Team: Marketing Campaign Approval
Team Lead: Marketing Director
Members:
  - Marketing Manager
  - Finance Manager
  - Legal Advisor
  - Brand Manager
```

**Workflow:**
1. Marketing creates PO for campaign materials
2. Assigned to "Marketing Campaign Approval" team
3. All 4 members review
4. Marketing Manager approves (campaign alignment)
5. Finance Manager approves (budget)
6. Legal Advisor approves (compliance)
7. Brand Manager approves (brand guidelines)
8. PO confirmed after all approvals

**Result:** Cross-functional review ensures compliance and alignment.

---

### Use Case 5: Rejection and Revision

**Business Need:** PO needs revision after rejection.

**Workflow:**
1. PO created and assigned to team
2. Team Member A approves
3. Team Member B reviews and rejects (found better vendor)
4. PO status shows rejection
5. Purchaser revises PO with new vendor
6. Team Member B changes rejection to approval
7. All approvals complete
8. PO confirmed

**Result:** Collaborative improvement of purchase decisions.

---

## Best Practices

### 1. Team Design

✅ **Do:**
- Create teams based on departments or purchase types
- Assign clear roles to team members
- Set appropriate team leads with authority
- Use descriptive short codes (e.g., "IT_HW", "HR_EQUIP")

❌ **Don't:**
- Create too many teams (hard to manage)
- Assign team leads without proper authority
- Use generic names that don't indicate purpose

### 2. Member Selection

✅ **Do:**
- Include all necessary stakeholders
- Keep teams small (3-5 members ideal)
- Assign members with relevant expertise
- Use roles to clarify responsibilities

❌ **Don't:**
- Add unnecessary approvers (slows process)
- Include members who rarely check Odoo
- Create teams with conflicting interests

### 3. Approval Process

✅ **Do:**
- Review POs promptly
- Provide feedback when rejecting
- Use team lead override only when necessary
- Document override reasons

❌ **Don't:**
- Approve without reviewing details
- Reject without explanation
- Override approvals routinely
- Ignore pending approvals

### 4. Amount Limits

✅ **Do:**
- Set appropriate min/max amounts
- Align limits with company policies
- Review limits periodically
- Escalate high-value purchases

❌ **Don't:**
- Set limits too low (creates bottlenecks)
- Set limits too high (defeats purpose)
- Ignore amount-based workflows

### 5. Communication

✅ **Do:**
- Notify team members of new POs
- Discuss rejections with purchasers
- Coordinate urgent approvals
- Review team performance regularly

---

## FAQ

### Q1: Can I approve a PO multiple times?

**A:** No, each team member can only approve or reject once per PO. However, you can change your decision (from approve to reject or vice versa) if needed.

### Q2: What happens if a team member leaves the company?

**A:** Remove them from the team. Existing POs will keep their approval routes, but new POs won't include them. For existing POs, the team lead can override if needed.

### Q3: Can I have different approval teams for different vendors?

**A:** Yes, you can create vendor-specific teams or assign teams manually per PO. The system doesn't automatically assign teams based on vendors.

### Q4: What if I need to change the approval team after creating a PO?

**A:** You can change the team, but this will:
- Delete existing approval routes
- Create new routes for the new team
- Reset all approval statuses

**Note:** Only change teams before any approvals are given.

### Q5: Can non-team members see approval status?

**A:** Yes, anyone with access to the PO can see the approval status in the "Approve Route" tab. However, only team members can approve/reject.

### Q6: How do I know if a PO is waiting for my approval?

**A:** 
- Check your Purchase Orders list
- Look for POs with your team assigned
- Check the "Approve Route" tab
- Look for your name with "Pending" status

### Q7: Can I set up automatic team assignment?

**A:** Currently, teams must be assigned manually. However, you can set a default team that auto-assigns to new POs.

### Q8: What's the difference between rejecting and cancelling a PO?

**A:** 
- **Reject (in approval):** Cancels your approval, prevents PO confirmation
- **Cancel PO:** Completely cancels the purchase order

### Q9: Can team leads see who approved/rejected?

**A:** Yes, team leads can see all approval statuses in the "Approve Route" tab, including who approved, rejected, or is still pending.

### Q10: How do I handle urgent purchases?

**A:** 
1. Create the PO with appropriate team
2. Notify team members of urgency
3. If still too slow, team lead can override and confirm directly
4. Document the reason for override

---

## Troubleshooting

### Issue: Approve button not visible

**Possible Causes:**
- User is not a member of the assigned team
- PO is not in draft/sent/to approve state
- User doesn't have purchase user permissions

**Solution:**
- Verify team membership
- Check PO state
- Verify user permissions

### Issue: PO cannot be confirmed

**Possible Causes:**
- Not all team members have approved
- User is not the team lead trying to override

**Solution:**
- Check "Approve Route" tab for pending approvals
- Have team lead confirm if urgent
- Wait for all approvals

### Issue: Approval routes not created

**Possible Causes:**
- Team has no members
- Team was assigned after PO creation (should work, but check)
- Database issue

**Solution:**
- Verify team has members
- Try reassigning the team
- Check Odoo logs for errors

### Issue: Team lead cannot override

**Possible Causes:**
- User is not set as team lead
- PO state doesn't allow confirmation
- Permission issue

**Solution:**
- Verify team lead assignment
- Check PO state
- Verify user has purchase manager permissions

---

## Additional Resources

- **Module Documentation:** See README.md
- **Odoo Purchase Documentation:** [Odoo Official Docs](https://www.odoo.com/documentation/19.0/applications/purchase.html)
- **Support:** Contact iTech Co. for module-specific support

---

**Version:** 19.0.1.0  
**Last Updated:** December 2025  
**Author:** iTech Co.


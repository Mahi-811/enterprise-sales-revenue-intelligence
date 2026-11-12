# Row-Level Security (RLS) & Governance Guide

## 1. Governance & Security Overview
The **Enterprise Sales & Revenue Intelligence System** implements dual security architectures to enforce data privacy and compliance:
1. **Static Regional Roles:** Fast, role-based access for macro-regional managers (Americas, EMEA, APAC).
2. **Dynamic Organizational Security:** User Principal Name (`USERPRINCIPALNAME()`) mapping via `UserSecurityMapping` supporting granular territory isolation and global administration.

---

## 2. Dynamic Security Implementation

### UserSecurityMapping Table Schema
| Field Name | Type | Description |
| :--- | :--- | :--- |
| `UserEmail` | Text | Entra ID (Azure AD) corporate email matching `USERPRINCIPALNAME()`. |
| `TerritoryKey` | Integer | Authorized territory. Value `0` indicates unrestricted enterprise administrator. |
| `Role` | Text | Business title / functional role description. |

### Dynamic DAX Filter Expression
Applied to `UserSecurityMapping`:
```dax
[UserEmail] == USERPRINCIPALNAME() || [TerritoryKey] == 0
```
Because the relationship between `UserSecurityMapping` and `DimTerritory` has **cross-filter direction set to Both** and **Apply security filter in both directions enabled**, filtering `UserSecurityMapping` automatically filters `DimTerritory`, which cascades down through 1:M relationships to `FactSales` and `FactTargets`.

---

## 3. Static Regional Roles
* **Role Name: `Americas_Region`**
  ```dax
  [Region] == "Americas"
  ```
  *Grants visibility into North America East (1), North America West (2), and Latin America (6).*
* **Role Name: `EMEA_Region`**
  ```dax
  [Region] == "EMEA"
  ```
  *Grants visibility into Europe Central (3) and Europe North & UK (4).*
* **Role Name: `APAC_Region`**
  ```dax
  [Region] == "APAC"
  ```
  *Grants visibility into Asia Pacific East (5).*

---

## 4. How to Test RLS in Power BI Desktop
1. Open the project in **Power BI Desktop**.
2. Navigate to the **Modeling** ribbon tab.
3. Click **View As**.
4. Test Static Roles: Check **Americas_Region** and click **OK**. Verify that all charts and cards only show Americas data.
5. Test Dynamic RLS:
   - Check **Dynamic_Territory_Security**.
   - Check **Other User** and enter: `astrid.lindgren@enterprisegroup.com`.
   - Click **OK**. Verify that only EMEA data is visible.
   - Enter `executive@enterprisegroup.com`. Verify that full global data is accessible.

---

## 5. Deployment & Power BI Service Role Assignment
1. Publish the report to the dedicated Power BI Service Workspace.
2. In the workspace, navigate to the **Semantic Model** &gt; click **Security**.
3. Under the **Row-Level Security** configuration:
   - For **Americas_Region**: Assign the Entra ID security group `SG-Sales-Americas-Managers`.
   - For **EMEA_Region**: Assign the Entra ID security group `SG-Sales-EMEA-Managers`.
   - For **APAC_Region**: Assign the Entra ID security group `SG-Sales-APAC-Managers`.
   - For **Dynamic_Territory_Security**: Assign the enterprise all-staff group `SG-Sales-Field-Representatives`.
4. Click **Save**.
5. Use **Test as role** in Power BI Service to perform post-deployment verification.

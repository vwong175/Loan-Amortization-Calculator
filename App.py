import numpy
import numpy_financial as npf

# Payment amount stays fixed
def calculatePaymentAmount(totalLoanAmount, annualInterestRate, termLength):
  ratePerMonth = (annualInterestRate / 100) / 12
  nper = termLength * 12
  pv = totalLoanAmount * -1

  monthlyPaymentAmount = npf.pmt(ratePerMonth,nper,pv)
  monthlyPaymentAmount = round(monthlyPaymentAmount, 2) 
  return monthlyPaymentAmount 

def calculateInterestOfMonth(previousBalance, annualInterestRate):
  ratePerMonth = (annualInterestRate / 100) / 12
  interestOfMonth = previousBalance * ratePerMonth
  interestOfMonth = round(interestOfMonth, 2)
  return interestOfMonth

def cumulativeInterest(listOflods, interest):
  sum_of_interests = 0
  for month_data in listOflods:
    interestDict = month_data[1]
    previous_int = interestDict["f"].strip("$")
    previous_int = float(previous_int)
    sum_of_interests += previous_int
  sum_of_interests += interest # Add the current month's interest onto the cumulative
  sum_of_interests = round(sum_of_interests, 2)
  return sum_of_interests

# Principal paid of that month
def principalOfMonth(annualInterestRate, pmt, previousBalance):
  interest = calculateInterestOfMonth(previousBalance, annualInterestRate)
  principalPaid = pmt - interest
  principalPaid = round(principalPaid, 2)
  return principalPaid

def cumulativePrincipalPaid(listOflods, principal):
  sum_of_principals = 0
  for month_data in listOflods:
    principalDict = month_data[3]
    previous_principal = principalDict["f"].strip("$")
    previous_principal = float(previous_principal)
    sum_of_principals += previous_principal
  sum_of_principals += principal # Add the current month's principal into the cumulative
  sum_of_principals = round(sum_of_principals, 2)
  return sum_of_principals

def currentBalance(principal, previousBalance):
  currentBalance = previousBalance - principal 
  currentBalance = round(currentBalance, 2)
  return currentBalance


def row(totalLoanAmount, annualInterestRate, termLength, previousBalance, up_to_current_data):
  ret_val = [{"f":"$"},{"f":"$"},{"f":"$"},{"f":"$"},{"f":"$"},{"f":"$"}]

  pmt = calculatePaymentAmount(totalLoanAmount, annualInterestRate, termLength)
  monthInterest = calculateInterestOfMonth(previousBalance, annualInterestRate)
  sumOfInterest = cumulativeInterest(up_to_current_data, monthInterest)
  monthPrincipal = principalOfMonth(annualInterestRate, pmt, previousBalance)
  sumOfPrincipalPaid = cumulativePrincipalPaid(up_to_current_data, monthPrincipal)
  monthBalance = currentBalance(monthPrincipal, previousBalance)

  ret_val[0] = {"f":"$" + str(pmt)}
  ret_val[1] = {"f":"$" + str(monthInterest)}
  ret_val[2] = {"f":"$" + str(sumOfInterest)}
  ret_val[3] = {"f":"$" + str(monthPrincipal)}
  ret_val[4] = {"f":"$" + str(sumOfPrincipalPaid)}
  ret_val[5] = {"f":"$" + str(monthBalance)}
  
  return ret_val


def data_by_months(diction):
  totalLoanAmount = int(diction["loan_amount"])
  annualInterestRate = float(diction["annual_interest_rate"])
  termLength = int(diction["loan_term_length"])

  up_to_current_data = [] # store up to the current month of loop's loan data for cumulative interest & principal
  nper = termLength * 12
  previous_month_data = {} #quick lookup of the previous month's list of dictionary values
  
  for month_number in range(1,nper+1):
    if month_number == 1:
      previousBalance = totalLoanAmount
      month_data = row(totalLoanAmount, annualInterestRate, termLength, previousBalance, up_to_current_data)
      up_to_current_data.append(month_data)
      previous_month_data = month_data
    else:
      previousBalanceDict = previous_month_data[5] #will be {"f": "$balance"}
      previousBalance = float(previousBalanceDict["f"].strip("$"))
      month_data = row(totalLoanAmount, annualInterestRate, termLength, previousBalance, up_to_current_data)
      up_to_current_data.append(month_data)
      previous_month_data = month_data
    
  return up_to_current_data

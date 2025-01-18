#include "bank-demo.hpp"

#include <iostream>
#include <string>
#include <unordered_map>

#include "tracer.hpp"

class Account
{
   public:
    Account(const std::string& account_number, double balance)
        : account_number(account_number), balance(balance)
    {
    }

    void deposit(double amount)
    {
        TRACE;
        balance += amount;
    }

    void withdraw(double amount)
    {
        TRACE;
        if (amount > balance)
        {
            throw std::invalid_argument("Insufficient funds");
        }
        balance -= amount;
    }

   private:
    std::string account_number;
    double balance;
};

class Transaction
{
   public:
    Transaction(const std::string& transaction_type, double amount)
        : transaction_type(transaction_type), amount(amount)
    {
    }

    void process(Account& account) const
    {
        TRACE;
        if (transaction_type == "deposit")
        {
            account.deposit(amount);
        }
        else if (transaction_type == "withdrawal")
        {
            account.withdraw(amount);
        }
    }

   private:
    std::string transaction_type;
    double amount;
};

class Bank
{
   public:
    Bank() : accounts() {}

    void create_account(const std::string& account_number,
                        double initial_balance)
    {
        TRACE;
        accounts.emplace(account_number,
                         Account(account_number, initial_balance));
    }

    void process_transaction(const Transaction& transaction,
                             const std::string& account_number)
    {
        TRACE;
        auto it = accounts.find(account_number);
        if (it != accounts.end())
        {
            transaction.process(it->second);
        }
        else
        {
            throw std::invalid_argument("Account not found");
        }
    }

   private:
    std::unordered_map<std::string, Account> accounts;
};

void bank_demo()
{
    TRACE;
    Bank bank;
    bank.create_account("12345", 1000.0);
    bank.create_account("67890", 500.0);

    Transaction transaction("withdrawal", 200.0);
    bank.process_transaction(transaction, "12345");

    transaction = Transaction("deposit", 200.0);
    bank.process_transaction(transaction, "67890");
}

import json
import os
import re
from datetime import datetime
from typing import List, Dict, Optional

class Contact:
    """Represents a single contact with all necessary information."""
    
    def __init__(self, name: str, phone: str, email: str = "", address: str = ""):
        self.id = self._generate_id()
        self.name = name.strip()
        self.phone = phone.strip()
        self.email = email.strip()
        self.address = address.strip()
        self.created_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.updated_date = self.created_date
    
    def _generate_id(self) -> int:
        """Generate a unique ID for the contact."""
        return int(datetime.now().timestamp() * 1000) % 100000
    
    def to_dict(self) -> Dict:
        """Convert contact to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'name': self.name,
            'phone': self.phone,
            'email': self.email,
            'address': self.address,
            'created_date': self.created_date,
            'updated_date': self.updated_date
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Contact':
        """Create contact from dictionary."""
        contact = cls(data['name'], data['phone'], data['email'], data['address'])
        contact.id = data['id']
        contact.created_date = data['created_date']
        contact.updated_date = data['updated_date']
        return contact
    
    def update_details(self, name: str = None, phone: str = None, email: str = None, address: str = None):
        """Update contact details and timestamp."""
        if name is not None:
            self.name = name.strip()
        if phone is not None:
            self.phone = phone.strip()
        if email is not None:
            self.email = email.strip()
        if address is not None:
            self.address = address.strip()
        self.updated_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def __str__(self) -> str:
        """String representation of the contact."""
        return f"""
ID: {self.id}
Name: {self.name}
Phone: {self.phone}
Email: {self.email if self.email else 'Not provided'}
Address: {self.address if self.address else 'Not provided'}
Created: {self.created_date}
Updated: {self.updated_date}
{'─' * 50}"""

class ContactManager:
    """Main contact management class with all CRUD operations."""
    
    def __init__(self, filename: str = "contacts.json"):
        self.filename = filename
        self.contacts: List[Contact] = []
        self.load_contacts()
    
    def add_contact(self, name: str, phone: str, email: str = "", address: str = "") -> Contact:
        """Add a new contact to the list."""
        # Validate required fields
        if not name.strip():
            raise ValueError("Name cannot be empty")
        if not phone.strip():
            raise ValueError("Phone number cannot be empty")
        
        # Check for duplicate phone numbers
        if self.get_contact_by_phone(phone.strip()):
            raise ValueError("A contact with this phone number already exists")
        
        contact = Contact(name, phone, email, address)
        self.contacts.append(contact)
        self.save_contacts()
        return contact
    
    def get_contact_by_id(self, contact_id: int) -> Optional[Contact]:
        """Get a contact by its ID."""
        for contact in self.contacts:
            if contact.id == contact_id:
                return contact
        return None
    
    def get_contact_by_phone(self, phone: str) -> Optional[Contact]:
        """Get a contact by phone number."""
        for contact in self.contacts:
            if contact.phone == phone.strip():
                return contact
        return None
    
    def search_contacts(self, query: str) -> List[Contact]:
        """Search contacts by name or phone number."""
        query = query.strip().lower()
        results = []
        
        for contact in self.contacts:
            if (query in contact.name.lower() or 
                query in contact.phone or 
                query in contact.email.lower() or 
                query in contact.address.lower()):
                results.append(contact)
        
        return results
    
    def update_contact(self, contact_id: int, name: str = None, phone: str = None, 
                      email: str = None, address: str = None) -> bool:
        """Update contact details."""
        contact = self.get_contact_by_id(contact_id)
        if not contact:
            return False
        
        # Check for duplicate phone if phone is being updated
        if phone and phone.strip() != contact.phone:
            existing_contact = self.get_contact_by_phone(phone.strip())
            if existing_contact and existing_contact.id != contact_id:
                raise ValueError("A contact with this phone number already exists")
        
        contact.update_details(name, phone, email, address)
        self.save_contacts()
        return True
    
    def delete_contact(self, contact_id: int) -> bool:
        """Delete a contact from the list."""
        contact = self.get_contact_by_id(contact_id)
        if contact:
            self.contacts.remove(contact)
            self.save_contacts()
            return True
        return False
    
    def get_all_contacts(self) -> List[Contact]:
        """Get all contacts sorted by name."""
        return sorted(self.contacts, key=lambda x: x.name.lower())
    
    def get_contact_count(self) -> int:
        """Get total number of contacts."""
        return len(self.contacts)
    
    def save_contacts(self):
        """Save contacts to JSON file."""
        try:
            with open(self.filename, 'w') as f:
                json.dump([contact.to_dict() for contact in self.contacts], f, indent=2)
        except Exception as e:
            print(f"Error saving contacts: {e}")
    
    def load_contacts(self):
        """Load contacts from JSON file."""
        try:
            if os.path.exists(self.filename):
                with open(self.filename, 'r') as f:
                    data = json.load(f)
                    self.contacts = [Contact.from_dict(contact_data) for contact_data in data]
        except Exception as e:
            print(f"Error loading contacts: {e}")
            self.contacts = []

class ContactApp:
    """Main application class with user interface."""
    
    def __init__(self):
        self.contact_manager = ContactManager()
    
    def display_menu(self):
        """Display the main menu."""
        print("\n" + "="*60)
        print("📞 CONTACT MANAGEMENT SYSTEM")
        print("="*60)
        print("1. 👤 Add New Contact")
        print("2. 📋 View All Contacts")
        print("3. 🔍 Search Contacts")
        print("4. ✏️  Update Contact")
        print("5. 🗑️  Delete Contact")
        print("6. 📊 Contact Statistics")
        print("7. 💾 Save Contacts")
        print("8. ❌ Exit")
        print("="*60)
    
    def validate_phone(self, phone: str) -> bool:
        """Validate phone number format."""
        # Remove all non-digit characters for validation
        digits_only = re.sub(r'\D', '', phone)
        return len(digits_only) >= 10
    
    def validate_email(self, email: str) -> bool:
        """Validate email format."""
        if not email:
            return True  # Email is optional
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def get_contact_input(self) -> Dict[str, str]:
        """Get contact information from user with validation."""
        print("\n📝 CONTACT INFORMATION")
        print("-" * 30)
        
        # Get name (required)
        while True:
            name = input("Enter contact name: ").strip()
            if name:
                break
            print("❌ Name cannot be empty!")
        
        # Get phone (required)
        while True:
            phone = input("Enter phone number: ").strip()
            if phone and self.validate_phone(phone):
                break
            print("❌ Please enter a valid phone number (at least 10 digits)!")
        
        # Get email (optional)
        while True:
            email = input("Enter email address (optional): ").strip()
            if not email or self.validate_email(email):
                break
            print("❌ Please enter a valid email address!")
        
        # Get address (optional)
        address = input("Enter address (optional): ").strip()
        
        return {
            'name': name,
            'phone': phone,
            'email': email,
            'address': address
        }
    
    def add_contact_interactive(self):
        """Interactive contact addition."""
        print("\n👤 ADD NEW CONTACT")
        print("-" * 30)
        
        try:
            contact_data = self.get_contact_input()
            contact = self.contact_manager.add_contact(**contact_data)
            print(f"\n✅ Contact added successfully!")
            print(f"Contact ID: {contact.id}")
            print(f"Name: {contact.name}")
            print(f"Phone: {contact.phone}")
        except ValueError as e:
            print(f"❌ Error: {e}")
    
    def view_all_contacts(self):
        """Display all contacts."""
        contacts = self.contact_manager.get_all_contacts()
        if not contacts:
            print("\n📭 No contacts found!")
            return
        
        print(f"\n📋 ALL CONTACTS ({len(contacts)} total)")
        print("="*60)
        
        # Display in a compact format for the list view
        print(f"{'ID':<6} {'Name':<20} {'Phone':<15} {'Email':<25}")
        print("-" * 70)
        
        for contact in contacts:
            email_display = contact.email[:22] + "..." if len(contact.email) > 25 else contact.email
            print(f"{contact.id:<6} {contact.name:<20} {contact.phone:<15} {email_display:<25}")
        
        print(f"\n💡 Use 'Search Contacts' to view detailed information")
    
    def search_contacts_interactive(self):
        """Interactive contact search."""
        print("\n🔍 SEARCH CONTACTS")
        print("-" * 30)
        
        query = input("Enter search term (name, phone, email, or address): ").strip()
        if not query:
            print("❌ Search term cannot be empty!")
            return
        
        results = self.contact_manager.search_contacts(query)
        if not results:
            print(f"\n📭 No contacts found matching '{query}'")
            return
        
        print(f"\n🔍 SEARCH RESULTS ({len(results)} found)")
        print("="*60)
        
        for contact in results:
            print(contact)
    
    def update_contact_interactive(self):
        """Interactive contact update."""
        print("\n✏️ UPDATE CONTACT")
        print("-" * 30)
        
        try:
            contact_id = int(input("Enter contact ID to update: "))
        except ValueError:
            print("❌ Invalid contact ID!")
            return
        
        contact = self.contact_manager.get_contact_by_id(contact_id)
        if not contact:
            print("❌ Contact not found!")
            return
        
        print(f"\nCurrent contact details:")
        print(contact)
        
        print("\nWhat would you like to update?")
        print("1. Name")
        print("2. Phone")
        print("3. Email")
        print("4. Address")
        print("5. All Details")
        
        choice = input("Select option (1-5): ").strip()
        
        try:
            if choice == "1":
                new_name = input("Enter new name: ").strip()
                if new_name:
                    if self.contact_manager.update_contact(contact_id, name=new_name):
                        print("✅ Contact name updated successfully!")
                    else:
                        print("❌ Failed to update contact name!")
                else:
                    print("❌ Name cannot be empty!")
            
            elif choice == "2":
                while True:
                    new_phone = input("Enter new phone number: ").strip()
                    if new_phone and self.validate_phone(new_phone):
                        if self.contact_manager.update_contact(contact_id, phone=new_phone):
                            print("✅ Contact phone updated successfully!")
                        else:
                            print("❌ Failed to update contact phone!")
                        break
                    print("❌ Please enter a valid phone number!")
            
            elif choice == "3":
                while True:
                    new_email = input("Enter new email address: ").strip()
                    if not new_email or self.validate_email(new_email):
                        if self.contact_manager.update_contact(contact_id, email=new_email):
                            print("✅ Contact email updated successfully!")
                        else:
                            print("❌ Failed to update contact email!")
                        break
                    print("❌ Please enter a valid email address!")
            
            elif choice == "4":
                new_address = input("Enter new address: ").strip()
                if self.contact_manager.update_contact(contact_id, address=new_address):
                    print("✅ Contact address updated successfully!")
                else:
                    print("❌ Failed to update contact address!")
            
            elif choice == "5":
                contact_data = self.get_contact_input()
                if self.contact_manager.update_contact(contact_id, **contact_data):
                    print("✅ All contact details updated successfully!")
                else:
                    print("❌ Failed to update contact details!")
            
            else:
                print("❌ Invalid choice!")
        
        except ValueError as e:
            print(f"❌ Error: {e}")
    
    def delete_contact_interactive(self):
        """Interactive contact deletion."""
        print("\n🗑️ DELETE CONTACT")
        print("-" * 30)
        
        try:
            contact_id = int(input("Enter contact ID to delete: "))
        except ValueError:
            print("❌ Invalid contact ID!")
            return
        
        contact = self.contact_manager.get_contact_by_id(contact_id)
        if not contact:
            print("❌ Contact not found!")
            return
        
        print(f"\nContact to delete:")
        print(contact)
        
        confirm = input("\nAre you sure you want to delete this contact? (y/n): ").strip().lower()
        if confirm in ['y', 'yes']:
            if self.contact_manager.delete_contact(contact_id):
                print("✅ Contact deleted successfully!")
            else:
                print("❌ Failed to delete contact!")
        else:
            print("❌ Contact deletion cancelled.")
    
    def show_statistics(self):
        """Display contact statistics."""
        total_contacts = self.contact_manager.get_contact_count()
        
        print("\n📊 CONTACT STATISTICS")
        print("="*40)
        print(f"Total Contacts: {total_contacts}")
        
        if total_contacts > 0:
            contacts = self.contact_manager.get_all_contacts()
            
            # Count contacts with complete information
            with_email = sum(1 for c in contacts if c.email)
            with_address = sum(1 for c in contacts if c.address)
            
            print(f"Contacts with email: {with_email} ({with_email/total_contacts*100:.1f}%)")
            print(f"Contacts with address: {with_address} ({with_address/total_contacts*100:.1f}%)")
            
            # Show recent contacts
            recent_contacts = sorted(contacts, key=lambda x: x.created_date, reverse=True)[:3]
            print(f"\n📅 Recent Contacts:")
            for contact in recent_contacts:
                print(f"  • {contact.name} ({contact.created_date})")
    
    def save_contacts_manual(self):
        """Manually save contacts."""
        self.contact_manager.save_contacts()
        print("✅ Contacts saved successfully!")
    
    def run(self):
        """Main application loop."""
        print("🚀 Welcome to the Contact Management System!")
        print("Manage your contacts efficiently and securely!")
        
        while True:
            self.display_menu()
            
            try:
                choice = input("\nEnter your choice (1-8): ").strip()
                
                if choice == "1":
                    self.add_contact_interactive()
                elif choice == "2":
                    self.view_all_contacts()
                elif choice == "3":
                    self.search_contacts_interactive()
                elif choice == "4":
                    self.update_contact_interactive()
                elif choice == "5":
                    self.delete_contact_interactive()
                elif choice == "6":
                    self.show_statistics()
                elif choice == "7":
                    self.save_contacts_manual()
                elif choice == "8":
                    print("\n👋 Thank you for using the Contact Management System!")
                    print("Your contacts have been automatically saved.")
                    break
                else:
                    print("❌ Invalid choice! Please enter a number between 1-8.")
                
                input("\nPress Enter to continue...")
                
            except KeyboardInterrupt:
                print("\n\n👋 Application interrupted. Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ An error occurred: {e}")
                input("Press Enter to continue...")

if __name__ == "__main__":
    app = ContactApp()
    app.run()


const { MongoClient } = require('mongodb');
const bcrypt = require('bcrypt');
const { v4: uuidv4 } = require('uuid'); 

const url = 'mongodb://localhost:27017'; 
const dbName = 'library';

const data = {
  authors: [
    {
      _id: uuidv4(), 
      name: 'Author 1',
      birthdate: new Date('1980-01-01'),
      nationality: 'Nationality 1',
      biography: 'Biography of Author 1',
    },
  ],
  books: [
    {
      _id: uuidv4(), 
      title: 'Book 1',
      author_id: uuidv4(), 
      isbn: '1234567890',
      genre: 'Genre 1',
      published_date: new Date('2000-01-01'),
      copies_available: 5,
      total_copies: 10,
      keywords: ['Keyword 1', 'Keyword 2'],
      cover_image_url: 'https://example.com/book1-cover.jpg',
    },
   
  ],
  patrons: [
    {
      _id: uuidv4(), 
      first_name: 'John',
      middle_name: 'A.', 
      last_name: 'Doe',
      email: 'john.doe@example.com',
      password: bcrypt.hashSync('hashedPassword1', 10),
      address: '123 Main St',
      phone: '123-456-7890',
      member_since: new Date(),
      is_admin: true,
    },
    {
      _id: uuidv4(), 
      first_name: 'Eric',
      middle_name: 'B.', 
      last_name: 'Cartman',
      email: 'eric.cart@example.com',
      password: bcrypt.hashSync('balllls', 10), 
      address: '143 Colorado',
      phone: '192-425-5163',
      member_since: new Date(),
      is_admin: false,
    },
   
  ],
  transactions: [
    {
      _id: uuidv4(), 
      patron_id: uuidv4(),
      book_id: uuidv4(), 
      transaction_date: new Date(),
      transaction_type: 'borrow',
      due_date: new Date('2023-09-30'),
      returned_date: null,
      fine_amount: 0,
    },
  
  ],
  book_copies: [
    {
      _id: uuidv4(), 
      book_id: uuidv4(), 
      copy_number: 1,
      condition: 'Good',
      location: 'Shelf A',
    },
  
  ],
  reservations: [
    {
      _id: uuidv4(), 
      patron_id: uuidv4(), 
      book_id: uuidv4(), 
      reservation_date: new Date(),
      pickup_deadline: new Date('2023-10-15'),
    },
    
  ],
  fines: [
    {
      _id: uuidv4(), 
      patron_id: uuidv4(), 
      amount: 5.0,
      reason: 'Late book return',
      fine_date: new Date(),
    },
  ],
};

// async/await to connect and create the database and collections
async function createDatabase() {
  const client = new MongoClient(url, { useUnifiedTopology: true });
  try {
    await client.connect();
    const db = client.db(dbName);
    for (const collectionName of Object.keys(data)) {
      await db.collection(collectionName).insertMany(data[collectionName]);
    }
    console.log('Database and collections created successfully.');
  } catch (err) {
    console.error('Error creating database:', err);
  } finally {
    client.close();
  }
}
createDatabase();

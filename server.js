import express from 'express';
import { createClient } from '@supabase/supabase-js';
import dotenv from 'dotenv';

// Load environment variables
dotenv.config();

const app = express();
app.use(express.json()); // Middleware to parse JSON bodies

// Initialize Supabase Client
const supabaseUrl = process.env.SUPABASE_URL;
const supabaseAnonKey = process.env.SUPABASE_ANON_KEY;

if (!supabaseUrl || !supabaseAnonKey) {
  console.error("Missing Supabase environment variables.");
  process.exit(1);
}

const supabase = createClient(supabaseUrl, supabaseAnonKey);

/**
 * POST /api/leaderboard
 * Appends a new score and full name to the leaderboard
 */

app.post('/api/upload-csv', async (req, res) => {
  const records = req.body;

  if (!Array.isArray(records) || records.length === 0) {
    return res.status(400).json({
      error: 'Expected a non-empty array'
    });
  }

  try {
    const participants = records.map(record => ({
      team_name: record.team_name
    }));

    const { data, error } = await supabase
      .from('participants')
      .insert(participants)
      .select();

    if (error) {
      throw error;
    }

    return res.status(201).json({
      message: 'Participants uploaded successfully!',
      count: data.length
    });

  } catch (error) {
    return res.status(500).json({
      error: 'Failed to insert participants',
      details: error.message
    });
  }
});


// Start the server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Backend server running on port ${PORT}`);
});

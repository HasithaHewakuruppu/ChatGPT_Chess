import streamlit as st
import openai
import chess
import chess.svg
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize OpenAI API client with your key
openai.api_key = os.environ.get('OPENAI_API_KEY')

# Initialize game if not already done
if 'board' not in st.session_state:
    st.session_state.board = chess.Board()

# Initialize message history
if 'messages' not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": "Let's play chess!"}]

st.title('Chess with ChatGPT')

# Get the user's move
move = st.text_input('Enter your move (e.g., "e2e4"):')

if st.button('Make Move'):
    # Update the board with the user's move
    try:
        st.session_state.board.push_san(move)
        st.session_state.messages.append({"role": "user", "content": move})
    except ValueError:
        st.write("That's an invalid move. Try again.")
    else:
        # After a successful user move, ask ChatGPT for a move
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=st.session_state.messages  # Use the full message history
        )
        reply = response['choices'][0]['message']['content']
        
        try:
            st.session_state.board.push_san(reply)
            st.session_state.messages.append({"role": "system", "content": reply})
        except ValueError:
            st.write(f"ChatGPT suggested an invalid move: {reply}. You can continue playing.")

    # Clear the input field
    st.session_state.move = ''

# Display the chessboard
board_svg = chess.svg.board(board=st.session_state.board)
st.markdown(board_svg, unsafe_allow_html=True)

# Display game status
if st.session_state.board.is_checkmate():
    st.write("Checkmate!")
elif st.session_state.board.is_stalemate() or st.session_state.board.is_insufficient_material():
    st.write("It's a draw!")
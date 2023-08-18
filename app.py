import streamlit as st
import openai
import chess
import chess.svg
import os

# Initialize OpenAI API client with your key
openai.api_key = os.environ.get('OPENAI_API_KEY')

# Initialize game if not already done
if 'board' not in st.session_state:
    st.session_state.board = chess.Board()

# Initialize message history
if 'messages' not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": "Let's play chess!"}]

# Create two columns for layout
col1, col2 = st.columns(2)

# Displaying content in the left column (col1)
with col1:
    st.title('Chess with ChatGPT')

    # Create a form
    with st.form(key='move_form',clear_on_submit=True):
        # Get the user's move inside the form
        move = st.text_input('Enter your move (e.g., "e2e4"):')
        
        # Submit button for the form
        submit_move = st.form_submit_button('Submit Move')

        # Check if the move has been submitted
        if submit_move:
            # Update the board with the user's move
            try:
                st.session_state.board.push_san(move)
                st.session_state.messages.append({"role": "user", "content": move})

                # Check for game status after user's move
                if st.session_state.board.is_checkmate():
                    st.markdown("<h2><b>Checkmate! You win!</b></h2>", unsafe_allow_html=True)
                    st.stop()
                elif st.session_state.board.is_stalemate() or st.session_state.board.is_insufficient_material():
                    st.markdown("<h2><b>It's a draw!</b></h2>", unsafe_allow_html=True)
                    st.stop()
            except ValueError:
                st.write("That's an invalid move. Try again.")
            else:
                valid_move = False
                attempts = 0  # Counter to track attempts by ChatGPT
                max_attempts = 25

                while not valid_move and attempts < max_attempts:
                    response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=st.session_state.messages  # Use the full message history
                    )
                    reply = response['choices'][0]['message']['content']

                    try:
                        st.session_state.board.push_san(reply)
                        st.session_state.messages.append({"role": "system", "content": reply})

                        # Check for game status after ChatGPT's move
                        if st.session_state.board.is_checkmate():
                            st.markdown("<h2><b>Checkmate! ChatGPT wins!</b></h2>", unsafe_allow_html=True)
                            st.stop()
                        elif st.session_state.board.is_stalemate() or st.session_state.board.is_insufficient_material():
                            st.markdown("<h2><b>It's a draw!</b></h2>", unsafe_allow_html=True)
                            st.stop()

                        valid_move = True
                    except ValueError:
                        # If ChatGPT's move is invalid, increment attempts and ask again
                        attempts += 1

                if attempts == max_attempts:
                    st.write("ChatGPT failed to make a valid move after 25 tries. Please refresh and start again...")
                    st.write("I am sorry ChatGPT is not very good at chess yet. GPT4 should improve it, stay tuned!")

# Displaying the chessboard in the right column (col2)
with col2:
    # Display the chessboard
    board_svg = chess.svg.board(board=st.session_state.board)
    st.markdown(board_svg, unsafe_allow_html=True)

# Adding the footer
st.markdown("""
    <style>
        .footer {
            position: fixed;
            bottom: 10px;
            left: 50%;
            transform: translate(-50%, -50%);
            padding: 5px;
            background-color: black;
            border-radius: 5px;
        }
    </style>
    <div class="footer">Made by Hasitha Hewakuruppu</div>
""", unsafe_allow_html=True)

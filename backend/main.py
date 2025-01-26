import gemini as g
import timestamps as t


def main() -> None:

    
    file_name =  input("Enter Video File: ")
    timestamps = g.player_timestamp(key, file_name, ["LeBron James", "Stephen Curry"])
    t.create_name_timestamp(timestamps)


if __name__ == "__main__":
    main()
import backend.gemini as g
import backend.timestamps as t


def main() -> None:
    key = "enter api key"
    file_name =  input("Enter Video File: ")
    timestamps = g.player_timestamp(key, file_name)
    t.create_name_timestamp(timestamps)


if __name__ == "__main__":
    main()
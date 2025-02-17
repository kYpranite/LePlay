import { Textarea } from "./ui/textarea";
import {Card, CardContent, CardHeader, CardTitle} from "./ui/card";

export default function Instruction({handleAddInstruction}: {handleAddInstruction: (instruction: string) => void}) {

    const handleChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
        handleAddInstruction(e.target.value);
      };

    return (
        <Card className="m-10 border-solid border-gray-200 border-2 w-3/6 rounded-2xl shadow-sm">
            <CardHeader>
            <CardTitle>Instructions</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
                <Textarea
                    placeholder="Enter instruction here..."
                    className="h-[150px]"
                    onChange={handleChange}
                />
            </CardContent>
        </Card>
    )
}
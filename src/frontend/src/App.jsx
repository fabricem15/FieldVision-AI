import React, { useState, useEffect } from 'react';
import Typography from '@mui/joy/Typography';
import { FormControl, FormLabel, Stack, Button, Checkbox, Box, Select, Option, Input } from '@mui/joy';

function Home() {
    const fields = ["Pitcher ID", "Batter ID", "Year", "Pitch Number", "Bat score", "Field score", "Inning"];
    return (
        <Stack sx={{ backgroundColor: "#000000de", height: "100vh" }}>
            <Typography level='h1' variant="plain" sx={{ color: "#f1d6b7" }}>Field Vision AI</Typography>
            <Stack direction="row" justifyContent="space-around" spacing={12} alignItems={"center"}>
                <Box className="form" sx={{ padding: "1rem" }}>
                    {fields.map((field) => (
                        <>
                            <FormControl size="sm">
                                <FormLabel sx={{ color: 'white', marginBlock: '5px' }}>{field}:</FormLabel>
                                <Input placeholder={field} variant="soft" size='sm' sx={{ marginBlockEnd: '10px' }} />
                            </FormControl>
                        </>
                    ))}
                    <Stack direction='row' spacing={2}>
                        <Button color="success" size='sm'>Predict Hit Location</Button>
                        <Button variant='soft' size='sm'>Adapt to Game State</Button>
                    </Stack>

                </Box>
                <Box className="img">
                    <img src="baseball_field.png" alt="placeholder" className="fieldImg" />
                </Box>
            </Stack>
        </Stack>
    );
}

export default Home;